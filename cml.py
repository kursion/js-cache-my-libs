#!/bin/python3
import os, http.server, socketserver, hashlib, urllib.request, \
    configparser, argparse

parser = argparse.ArgumentParser(
        description='CacheMyLibs - Yves Lange')
parser.add_argument(
        '--verbosity', action="store_true",
        help='adding some verbosity')
ARGS = parser.parse_args()

# Settings
cfg_file = "config.ini"

def initConfig(config_filename):
    """ Creating the default configuration file """
    config = configparser.ConfigParser()
    config['DEFAULT'] = {}
    config['SERVER'] = {
            'port': 8666,
            'pid': "/var/run/cml/cml.pid",
            }
    config['CACHE'] = {
            'use-cache': "no",
            'cache-dir': "cache/"
            }
    CONFIG["CDN"] = {
            'cloudflare': "http://cdnjs.cloudflare.com/ajax/libs"
            }
    CONFIG["LIBS"] = {
            'jquery.min.js': "jquery/2.1.1-beta1/jquery.min.js",
            'react.js': "react/0.10.0/react.min.js"
            }
    with open(config_filename, 'w') as cfg: config.write(cfg)

def readConfig(config_filename):
    """ Reading the configuration file """
    config = configparser.ConfigParser()
    config.read(config_filename)
    if ARGS.verbosity:
        for sec in config.sections():
            print("[", sec, "]")
            for el in config[sec]:
                print(">", el, "\t:", config[sec][el])
    return config

# Configuration init
if not os.path.isfile(cfg_file): initConfig(cfg_file)
CONFIG = readConfig(cfg_file)


# HTTP Get Handler
Handler = http.server.SimpleHTTPRequestHandler
class MyHandler (Handler):
    cdnExts = ['js']

    def do_GET(self):
      """Serve a GET request."""
      f = self.send_head()
      if f:
        try:
            self.copyfile(f, self.wfile)
        finally:
            f.close()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Try to download from CDN and retry
            if path.split(".")[-1] in self.cdnExts and \
                    CONFIG["CACHE"].getboolean("use-cache"):
                f = self.attemptCDN(self.path)
            else: f = open(path, 'rb')
        except OSError:

            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def attemptCDN(self, path):
        """ Tries to get the CDN from localhost or download it
        from the CDN (cloudflare.com) """
        if path[1:] in CONFIG["LIBS"]: path = "/"+CONFIG["LIBS"][path[1:]]
        for cdnPrefix in CONFIG["CDN"]:
            cdnPath = CONFIG["CDN"][cdnPrefix]+path
            filename = CONFIG["CACHE"]["cache-dir"]+hashlib.md5(cdnPath.encode()).hexdigest()
            if ARGS.verbosity: print("Checking cache: ", path, "as", filename)
            f = self.getFile(filename)
            if f == None:
                if ARGS.verbosity: print("Get from", cdnPrefix, cdnPath)
                f = self.getPage(cdnPath, filename)
            if f != None:
                if ARGS.verbosity: print("Found", cdnPath, "from CDN")
                break
        return f

    def getFile(self, filename):
        """ Get file content if exists else returns None """
        if os.path.isfile(filename):
            f = open(filename, 'rb')
            return f
        return None

    def getPage(s, url, path):
        """ Get and write the content of a page to a file """
        # TODO: this might be simplified a bit
        f = urllib.request.urlopen(url)
        srcOnline = f.read().decode("utf-8")
        f.close()
        # TODO: this doesn't work as it should be
        if srcOnline == "":
            if ARGS.verbosity: print("Couldn't find from CDN at", url)
            return None

        f = open(path, 'w')
        f.write(srcOnline)
        f.close()

        f = open(path, 'rb')
        return f


# MAIN
PORT = int(CONFIG["SERVER"]["port"])
httpd = socketserver.TCPServer(("", PORT), MyHandler)
if ARGS.verbosity: print("serving at port", PORT)
httpd.serve_forever()






