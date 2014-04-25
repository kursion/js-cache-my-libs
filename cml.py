#!/bin/python3
import os,  socketserver
import config
import utils
import handler

# TODO: refactoring everything here !
class Cml:
    conf    = config.Main()
    ARGS    = conf.getArgs()
    CONFIG  = conf.getConfig()

    def check_pid(s, u, no_pid):
        if not no_pid:
            pid = str(os.getpid())
            if os.path.isfile(s.CONFIG["SERVER"]["pidfile"]):
                s.exit(u, s.CONFIG["SERVER"]["pidfile"]+
                        "already exists, exiting ", no_pid)
            else: open(s.CONFIG["SERVER"]["pidfile"], 'w').write(pid)

    def check_cache(s, u):
        if not os.path.exists(s.CONFIG["CACHE"]["cache-dir"]):
            u.print("Cache directory not found, creating",
                        s.CONFIG["CACHE"]["cache-dir"])
            os.mkdir(s.CONFIG["CACHE"]["cache-dir"])

    def exit(s, u, msg, no_pid):
        u.print("[<- ] Exiting:", msg)
        if not no_pid: os.unlink(s.CONFIG["SERVER"]["pidfile"])
        exit()

    def get_port(s, u):
        if s.ARGS.port: return int(s.ARGS.port)
        else: return int(s.CONFIG["SERVER"]["port"])

    def serve(s, u, PORT):
        # Init TCPServer
        try:
            httpd = socketserver.TCPServer(("", PORT), handler.MyHandler)
        except OSError:
            s.exit(u, "Error: ip already binded", s.ARGS.no_pid)

        u.print("serving at port", PORT)

        # Launching the server
        try: httpd.serve_forever()
        except KeyboardInterrupt: s.exit(u, "goodbye", s.ARGS.no_pid)

    def __init__(s):
        u = utils.Main(verbosity=s.ARGS.verbosity)
        s.check_pid(u, s.ARGS.no_pid)
        s.check_cache(u)
        s.serve(u, s.get_port(u))

# Python might start eating from this point
cml = Cml()


