class Main:
    verbosity = False

    def __init__(s, verbosity=False):
        s.verbosity = verbosity

    def print(s, *txt):
        """ Verbosity print
        should receive the args.parser with verbosity set """
        if s.verbosity:
            r = ""
            for e in txt: r += ' '+str(e)
            print(r)

