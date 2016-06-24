
from distutils import cmd

from pyqver import pyqver2
from pyqver import pyqverbase


class BaseCommand(cmd.Command):
    """Command is an abstract class that requires initialize_options, finalize_options,
    and user_options to be defined.  This class provides stub definitions and other
    utility methods.
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class PyqverChecker(object):
    name = "pyqverChecker"
    version = "1.3"
    min_version = "2.5"

    def __init__(self, tree, filename, *args, **kwargs):
        self.tree = tree
        self.filename = filename

        self.args = args
        self.kwargs = kwargs

        self.results = []

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--min-version', default="2.5", action='store',
                          type=str, help="The min version of python to check. For ex, '2.6' will show code only supported in 2.7 or newer")
        parser.config_options.append('min-version')

    @classmethod
    def parse_options(cls, options):
        cls.min_version = tuple(map(int, options.min_version.split(".")))

    def usage_exit(self):
        pass

    def begin(self, *args):
        pass

    def item(self, filename, version, reasons):
        for reason in reasons:
            ver = ".".join(map(str, version))
            err_ver = "".join(map(str, version))
            msg = "V%s0 (%s) %s" % (err_ver, ver, reason[1])
            line_number = reason[0]
            offset = 0
            ret = (line_number, offset, msg, type(self))
            self.results.append(ret)

    # yield ret = (lineno, col_offset, msg, self)
    def run(self):
        self.results = []

        # FIXME: get these monkeypatching globals off this module flaking plane
        pyqverbase._printer = self
        pyqverbase._min_version = self.min_version
        pyqver2._allow_caught_import_errors = True

        pyqverbase.evaluate_file(self.filename, pyqver2.get_versions)
        for line_number, column_number, message, checker_name in self.results:
            yield line_number, column_number, message, checker_name
