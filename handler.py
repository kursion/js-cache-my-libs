import http.server, os, hashlib, urllib.request, time
import utils, config

# HTTP Get Handler
class MyHandler (http.server.SimpleHTTPRequestHandler):
    # TODO: find another way to pass those things from cml.py
    conf   = config.Main()
    ARGS   = conf.getArgs()
    CONFIG = conf.getConfig()
    u      = utils.Main(ARGS.verbosity)

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
            tS = time.time()*1000
            if self.CONFIG["CACHE"].getboolean("use-cache"):
                f = self.attemptCDN(self.path)
            else: f = open(path, 'rb')
            tE = time.time()*1000
            self.u.print("# Job done in:", tE-tS, "ms")
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

    def attemptCDN(s, path):
        """ Tries to get the CDN from localhost or download it
        from the CDN (cloudflare.com) """
        u = s.u

        if path[1:] in s.CONFIG["LIBS"]:
            path = "/"+s.CONFIG["LIBS"][path[1:]]

        for cdnPrefix in s.CONFIG["CDN"]:
            cdnPath = s.CONFIG["CDN"][cdnPrefix]+path
            filename = s.CONFIG["CACHE"]["cache-dir"]+\
                    hashlib.md5(cdnPath.encode()).hexdigest()
            u.print("Checking cache: ", cdnPath, "as", filename)
            f = s.getFile(filename)
            if f != None:
                u.print("Found in cache at", filename)
                return f

        # Was not in cache, get it from CDN
        for cdnPrefix in s.CONFIG["CDN"]:
            cdnPath = s.CONFIG["CDN"][cdnPrefix]+path
            filename = s.CONFIG["CACHE"]["cache-dir"]+\
                    hashlib.md5(cdnPath.encode()).hexdigest()
            u.print("Get from", cdnPrefix, cdnPath)
            f = s.getPage(cdnPath, filename)
            if f != None:
                u.print("Found", cdnPath, "from CDN and store in ",
                        filename)
                break
            else:
                u.print("Not found from", cdnPath)
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

