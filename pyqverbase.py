# Note to devs: Keep backwards compatibility with Python 2.3 AND 3.0.

import sys

def uniq(a):
    """
    Removes duplicates from a list. Elements are ordered by the original
    order of their first occurrences.

    In terms of Python 2.4 and later, this is equivalent to list(set(a)).
    """
    if len(a) == 0:
        return []
    else:
        return [a[0]] + uniq([x for x in a if x != a[0]])

def parse_args(printers, DefaultMinVersion):
    # Initializing default arguments
    printer = printers['compact']
    MinVersion = DefaultMinVersion
    files = []

    # Parsing options and arguments
    i = 1
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--test":
            import doctest
            doctest.testmod()
            sys.exit(0)
        # Whether reasons should be output
        elif a == "-v" or a == "--verbose":
            printer = printers['verbose']
        # Lint-style output
        elif a == "-l" or a == "--lint":
            printer = printers['lint']
        # The lowest version which may be output
        elif a == "-m" or a == "--min-version":
            i += 1
            MinVersion = tuple(map(int, sys.argv[i].split(".")))
        # The files which will be evaluated
        else:
            files.append(a)
        i += 1
    return printer, MinVersion, files

class Printer(object):
    """
    This class encapsulates a printing style for output.

    The begin and item members should be used by the client.
    """
    def __init__(self, begin, item):
        self.begin = begin
        self.item = item

