#!/bin/python3
import os, http.server, socketserver, hashlib, urllib.request

PORT = 8666

import configparser

def initConfig(config):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
            'port': 8666,
            'pid': "/var/run/cml/cml.pid",
            }
    config['CACHE'] = {
            'use-cache': "no",
            'cache-dir': "cache/"
            }
    with open(config, 'w') as configFile: config.write(configFile)

Handler = http.server.SimpleHTTPRequestHandler
class MyHandler (Handler):
    cacheDir = "cache/"
    cdnPrefix= "http://cdnjs.cloudflare.com/ajax/libs"
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
            if path.split(".")[-1] in self.cdnExts:
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
        cdnPath = self.cdnPrefix+path
        filename = self.cacheDir+hashlib.md5(cdnPath.encode()).hexdigest()
        f = self.getFile(filename)
        print("serving: ", path, "as", filename)
        if f == None:
            f = self.getPage(cdnPath, filename)
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

        f = open(path, 'w')
        f.write(srcOnline)
        f.close()

        f = open(path, 'rb')
        return f

initConfig("config.ini")

# MAIN
httpd = socketserver.TCPServer(("", PORT), MyHandler)
print("serving at port", PORT)
httpd.serve_forever()






