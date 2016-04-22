
import sys

# Base globals
_min_version = (0, 0)
_printer = None


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


def parse_args(printers, default_min_version):
    """
    Reads the command line arguments and sets up the system
    appropriately.

    Args:
      printers: A dictionary mapping at least 'verbose', 'lint'
          and 'compact' to a printer, which will be used for
          output
      default_min_version: The lowest Python version covered by
          the implementation.

    Returns:
      A nonempty list of files to be processed.

    If no filenames are given on the command line, this displays
    a usage note and exits the program.
    """

    # Initializing default arguments
    global _printer, _min_version
    _printer = printers['compact']
    _min_version = default_min_version
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
            _printer = printers['verbose']
        # Lint-style output
        elif a == "-l" or a == "--lint":
            _printer = printers['lint']
        # The lowest version which may be output
        elif a == "-m" or a == "--min-version":
            i += 1
            _min_version = tuple(map(int, sys.argv[i].split(".")))
        # The files which will be evaluated
        else:
            files.append(a)
        i += 1

    if not files:
        _printer.usage_exit()

    return files


class Printer(object):
    """
    This class encapsulates a printing style for output.

    All members are callbacks and should be used by the client.
    """
    def __init__(self, begin, item, syntax_error, usage_exit):
        self.begin = begin   # (filename, versions)
        self.item = item     # (filename, version, reasons)
        self.syntax_error = syntax_error   # (filename, err)
        self.usage_exit = usage_exit       # (), exits


def evaluate_files(files, get_versions):
    """
    Finds the minimal version for each script in a list and displays them.

    Args:
        files: A list of filenames, each file containing a script.
        get_versions: A function which accepts a whole script
            and finds all version issues.
    """
    for filename in files:
        evaluate_file(filename, get_versions)


def evaluate_file(fn, get_versions):
    """
    Finds the minimal version for a script and displays it.

    Args:
        fn: The name of the file containing the script.
        get_versions: A function which accepts a whole script
            and finds all version issues.
    """
    try:
        f = open(fn)
        source = f.read()
        f.close()
        ver = get_versions(source, fn)
        _printer.begin(fn, ver)
        for v in sorted([k for k in ver.keys() if k >= _min_version], reverse=True):
            reasons = [x for x in uniq(ver[v]) if x]
            _printer.item(fn, v, reasons)
    except SyntaxError as err:
        _printer.syntax_error(fn, err)


def run(printers, default_min_version, get_versions):
    """
    The main entry point of the base module.

    Args:
      printers: A dictionary mapping at least 'verbose', 'lint'
          and 'compact' to a printer, which will be used for
          output
      default_min_version: The lowest Python version covered by
          the implementation.
      get_versions: A function which accepts a whole script
            and finds all version issues.
    """
    files = parse_args(printers, default_min_version)
    evaluate_files(files, get_versions)
