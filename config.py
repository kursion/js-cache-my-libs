import os, configparser, argparse
import utils


class Main:
    """ Retrieve arguments and configuration from command line """
    args = None
    config = None

    def __init__(s):
        # Arguments init
        s.__initArgs()
        u = utils.Main(s.args.verbosity)

        # Configuration init
        if not os.path.isfile(s.args.config):
            u.print("Configuration file not found, creating",
                    s.args.config)
            s.__initConfig(s.args.config)
        s.__readConfig(s.args.config)
        for sec in s.config.sections():
            u.print("[", sec, "]")
            for el in s.config[sec]:
                u.print(">", el, ":", s.config[sec][el])

    def __initArgs(s):
        parser = argparse.ArgumentParser(
                description='CacheMyLibs - Yves Lange')
        parser.add_argument('-c',
                '--config', default='config.ini',
                help='specific configuration file')
        parser.add_argument('-p',
                '--port',
                help='server port (overwrite config file)')
        parser.add_argument(
                '--no-pid', action="store_true",
                help='ignore pid file')
        parser.add_argument('-v',
                '--verbosity', action="store_true",
                help='adding some verbosity')
        s.args = parser.parse_args()

    def getArgs(s):
        """ Get the arguments parser """
        return s.args

    def __initConfig(s, config_filename):
        """ Creating the default configuration file """
        config = configparser.ConfigParser()
        config['DEFAULT'] = {}
        config['SERVER'] = {
                'port': 8666,
                'pidfile': "cml.pid",
                }
        config['CACHE'] = {
                'use-cache': "yes",
                'cache-dir': "cache/"
                }
        config["CDN"] = {
                'cloudflare': "http://cdnjs.cloudflare.com/ajax/libs"
                }
        config["LIBS"] = {
                'jquery.min.js': "jquery/2.1.1-beta1/jquery.min.js",
                'react.js': "react/0.10.0/react.min.js"
                }
        with open(config_filename, 'w') as cfg: config.write(cfg)

    def __readConfig(s, config_filename):
        """ Reading the configuration file """
        s.config = configparser.ConfigParser()
        s.config.read(config_filename)

    def getConfig(s):
        """ Get the configuration """
        return s.config
