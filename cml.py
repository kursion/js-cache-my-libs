#!/bin/python3
import os, http.server, socketserver, hashlib, urllib.request, config
import utils

# TODO: refactoring everything here !
class Cml:
    ARGS = config.Main().getArgs()
    def __init__(s):
        print("INIT CML")
        if not os.path.exists(CONFIG["CACHE"]["cache-dir"]):
            u.print("Cache directory not found, creating",
                        CONFIG["CACHE"]["cache-dir"])
            os.mkdir(CONFIG["CACHE"]["cache-dir"])
a = Cml()


# HTTP Get Handler
Handler = http.server.SimpleHTTPRequestHandler
class MyHandler (Handler):

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
            if CONFIG["CACHE"].getboolean("use-cache"):
                f = self.attemptCDN(self.path)
            else: f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None

        if f == None:
            self.send_error(404, "File not found")
            return

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
            if ARGS.verbosity: print("Checking cache: ", cdnPath, "as", filename)
            f = self.getFile(filename)
            if f != None:
                print("Found in cache at", filename)
                return f

        # Was not in cache, get it from CDN
        for cdnPrefix in CONFIG["CDN"]:
            cdnPath = CONFIG["CDN"][cdnPrefix]+path
            filename = CONFIG["CACHE"]["cache-dir"]+hashlib.md5(cdnPath.encode()).hexdigest()
            if ARGS.verbosity:
                print("Get from", cdnPrefix, cdnPath)
            f = self.getPage(cdnPath, filename)
            if f != None:
                if ARGS.verbosity: print("Found", cdnPath, "from CDN and store in ", filename)
                break
            else:
                if ARGS.verbosity: print("Not found from", cdnPath)

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
        try:
            f = urllib.request.urlopen(url)
            srcOnline = f.read().decode("utf-8")
            f.close()
        except: return None

        f = open(path, 'w')
        f.write(srcOnline)
        f.close()

        f = open(path, 'rb')
        return f

# INIT
def init(CONFIG):
    pid = str(os.getpid())
    if os.path.isfile(CONFIG["SERVER"]["pidfile"]):
        print(CONFIG["SERVER"]["pidfile"],"already exists, exiting")
        exit()
    else: open(CONFIG["SERVER"]["pidfile"], 'w').write(pid)

# MAIN
init(CONFIG)
PORT = int(CONFIG["SERVER"]["port"])
try:
    httpd = socketserver.TCPServer(("", PORT), MyHandler)
except OSError:
    print("Error: ip already binded")
    os.unlink(CONFIG["SERVER"]["pidfile"])
    exit()

if ARGS.verbosity: print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    if ARGS.verbosity: print("exiting...")
    os.unlink(CONFIG["SERVER"]["pidfile"])
