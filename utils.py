class Main:
    verbosity = False

    def __init__(s, verbosity):
        s.verbosity = verbosity

    def print(s, *txt):
        """ Verbosity print
        should receive the args.parser with verbosity set """
        if s.verbosity: print(' '.join(txt))

