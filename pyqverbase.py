assert __name__ != '__main__'
# This is exclusively designed for inclusion by pyqver[23].py.

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

    All members are callbacks and should be used by the client.
    """
    def __init__(self, begin, item, syntax_error):
        self.begin = begin # (filename, versions)
        self.item = item # (filename, version, reasons)
        self.syntax_error = syntax_error # (filename, err)

def evaluate_files(printer, min_version, files, get_versions):
    for filename in files:
        evaluate_file(printer, min_version, filename, get_versions)
        
def evaluate_file(printer, min_version, fn, get_versions):
    try:
        f = open(fn)
        source = f.read()
        f.close()
        ver = get_versions(source, fn)
        printer.begin(fn, ver)
        for v in sorted([k for k in ver.keys() if k >= min_version], reverse=True):
            reasons = [x for x in uniq(ver[v]) if x]
            printer.item(fn, v, reasons)
    except SyntaxError as err:
        printer.syntax_error(fn, err)
    
