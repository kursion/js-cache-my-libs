#!/bin/python3
import os,  socketserver, hashlib, urllib.request
import config
import utils
import handler

# TODO: refactoring everything here !
class Cml:
    conf = config.Main()
    ARGS    = conf.getArgs()
    CONFIG  = conf.getConfig()
    def __init__(s):
        u = utils.Main(s.ARGS.verbosity)

        # Pid check
        pid = str(os.getpid())
        if os.path.isfile(s.CONFIG["SERVER"]["pidfile"]):
            u.print(s.CONFIG["SERVER"]["pidfile"],"already exists, exiting")
            exit()
        else: open(s.CONFIG["SERVER"]["pidfile"], 'w').write(pid)

        # Cache check
        if not os.path.exists(s.CONFIG["CACHE"]["cache-dir"]):
            u.print("Cache directory not found, creating",
                        s.CONFIG["CACHE"]["cache-dir"])
            os.mkdir(s.CONFIG["CACHE"]["cache-dir"])

        # MAIN
        PORT = int(s.CONFIG["SERVER"]["port"])
        try:
            httpd = socketserver.TCPServer(("", PORT), handler.MyHandler)
        except OSError:
            u.print("Error: ip already binded")
            os.unlink(s.CONFIG["SERVER"]["pidfile"])
            exit()

        u.print("serving at port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            u.print("exiting...")
            os.unlink(s.CONFIG["SERVER"]["pidfile"])
cml = Cml()


