#!/usr/bin/env python

# Note to devs: Keep backwards compatibility with Python 2.3.

import compiler
import platform
import sys

from pyqver import pyqverbase
from pyqver import regex_checker
from pyqver import version_data

DefaultMinVersion = (2, 3)


class NodeChecker(object):
    """
    A visitor, which traverses the syntax tree to find possible
    version issues.

    After traversal, the member vers will contain a dictionary
    mapping versions in a (maj,min) tuple format to lists of issues.
    An issue is a tuple of the line number where the issue resides,
    and a short message describing the issue.

    Python 2 specific: Traversal is achieved using the compiler.walk
                       function.
    """
    def __init__(self):
        self.vers = dict()
        self.vers[(2, 0)] = []
        self.allow_caught_import_errors = False
        self._import_error_handler = False

    def add(self, node, ver, msg):
        if ver not in self.vers:
            self.vers[ver] = []
        self.vers[ver].append((node.lineno, msg))

    def default(self, node):
        for child in node.getChildNodes():
            self.visit(child)

    def visitCallFunc(self, node):
        def rollup(n):
            if isinstance(n, compiler.ast.Name):
                return n.name
            elif isinstance(n, compiler.ast.Getattr):
                r = rollup(n.expr)
                if r:
                    return r + "." + n.attrname

        name = rollup(node.node)
        if name:
            v = version_data.Functions.get(name)
            if v is not None:
                self.add(node, v, "%s function" % name)

        self.default(node)

    def visitClass(self, node):
        if node.bases:
            self.add(node, (2, 2), "new-style class")

        for child in node.getChildNodes():
            if isinstance(child, compiler.ast.Decorators):
                # who to blame, the class or the decorator?
                self.add(node, (2, 6), "class decorator")

        self.default(node)

    def visitDecorators(self, node):
        for node in node.nodes:
            self.add(node, (2, 4), "decorator")
        self.default(node)

    def visitDictComp(self, node):
        self.add(node, (2, 7), "dictionary comprehension")
        self.default(node)

    def visitFloorDiv(self, node):
        self.add(node, (2, 2), "// operator")
        self.default(node)

    def visitFrom(self, node):
        v = version_data.StandardModules.get(node.modname)
        if v is not None:
            self.add(node, v, 'import of %s' % node.modname)

        for n in node.names:
            name = node.modname + "." + n[0]
            v = version_data.Functions.get(name)
            if v is not None:
                self.add(node, v, 'import of %s' % (name))

    def visitFunction(self, node):
        if node.decorators:
            self.add(node, (2, 4), "function decorator")
        self.default(node)

    def visitGenExpr(self, node):
        self.add(node, (2, 4), "generator expression")
        self.default(node)

    def visitGetattr(self, node):
        def is_format(node):
            return isinstance(node.expr, compiler.ast.Const) and \
                isinstance(node.expr.value, str) and node.attrname == "format"

        if is_format(node):
            self.add(node, (2, 6), "string literal .format()")
            if ',' in node.expr.value:
                self.add(node, (2, 7), "format specifier for thousand (comma)")

        self.default(node)

    def visitIfExp(self, node):
        self.add(node, (2, 5), "inline if expression")
        self.default(node)

    def visitImport(self, node):
        for n in node.names:
            v = version_data.StandardModules.get(n[0])
            if v is not None:
                if not self._import_error_handler:
                    self.add(node, v, 'import of %s that is not in a try/except ImportError' % n[0])
        self.default(node)

    def visitName(self, node):
        v = version_data.Identifiers.get(node.name)
        if v is not None:
            self.add(node, v, node.name)
        self.default(node)

    def visitReturn(self, node):
        self.default(node)

    def visitSet(self, node):
        self.add(node, (2, 7), "set literal")
        self.default(node)

    def visitSetComp(self, node):
        self.add(node, (2, 7), "set comprehension")
        self.default(node)

    def visitTryExcept(self, node):
        # Attempt to detect module imports protected by try/except ImportError
        for handler in node.handlers:
            # For multiple 'except (FooError, Foo2Errro)' handler[0]
            # can be a tuple
            exc_name = handler[0]
            if isinstance(exc_name, compiler.ast.Name) and \
                    exc_name.name == 'ImportError':
                self._import_error_handler = self.allow_caught_import_errors

        self.default(node)
        self._import_error_handler = False

    def visitTryFinally(self, node):
        # try/finally with a suite generates a Stmt node as the body,
        # but try/except/finally generates a TryExcept as the body
        if isinstance(node.body, compiler.ast.TryExcept):
            self.add(node, (2, 5), "try/except/finally")
        self.default(node)

    def visitWith(self, node):
        if isinstance(node.body, compiler.ast.With):
            self.add(node, (2, 7), "with statement with multiple contexts")
        else:
            self.add(node, (2, 5), "with statement")
        self.default(node)

    def visitYield(self, node):
        self.add(node, (2, 2), "yield expression")
        self.default(node)


def get_versions(source, filename=None):
    """Return information about the Python versions required for specific features.

    The return value is a dictionary with keys as a version number as a tuple
    (for example Python 2.6 is (2,6)) and the value are a list of features that
    require the indicated Python version.
    """
    tree = compiler.parse(source)
    checker = compiler.walk(tree, NodeChecker())
    line_checker = regex_checker.LineChecker(source)
    checker.vers.update(line_checker.vers)
    return checker.vers


def v27(source):
    if sys.version_info >= (2, 7):
        return qver(source)
    else:
        print >>sys.stderr, "Not all features tested, run --test with Python 2.7"
        return (2, 7)


def qver(source):
    """Return the minimum Python version required to run a particular bit of code."""

    return max(get_versions(source).keys())


def print_usage_and_exit():
    print >>sys.stderr, """Usage: %s [options] source ...

    Report minimum Python version required to run given source files.

    -m x.y or --min-version x.y (default 2.3)
        report version triggers at or above version x.y in verbose mode
    -v or --verbose
        print more detailed report of version triggers for each version
    -l or --lint
        print a report in the style of Lint, with line numbers
    """ % sys.argv[0]
    sys.exit(1)


def print_syntax_error(filename, err):
    print "%s: syntax error compiling with Python %s: %s" % (filename, platform.python_version(), err)


def print_verbose_begin(filename, versions):
    print filename


def print_verbose_item(filename, version, reasons):
    if reasons:
        # each reason is (lineno, message)
        print "\t%s\t%s" % (".".join(map(str, version)), ", ".join([r[1] for r in reasons]))

verbose_printer = pyqverbase.Printer(print_verbose_begin, print_verbose_item,
                                     print_syntax_error, print_usage_and_exit)


def print_lint_begin(filename, versions):
    pass


def print_lint_item(filename, version, reasons):
    for r in reasons:
        # each reason is (lineno, message)
        print "%s:%s: %s %s" % (filename, r[0], ".".join(map(str, version)), r[1])

lint_printer = pyqverbase.Printer(print_lint_begin, print_lint_item,
                                  print_syntax_error, print_usage_and_exit)


def print_compact_begin(filename, versions):
    print "%s\t%s" % (".".join(map(str, max(versions.keys()))), filename)


def print_compact_item(filename, version, reasons):
    pass

compact_printer = pyqverbase.Printer(print_compact_begin, print_compact_item,
                                     print_syntax_error, print_usage_and_exit)

printers = {'verbose': verbose_printer,
            'lint': lint_printer,
            'compact': compact_printer}


def main():
    pyqverbase.run(printers, DefaultMinVersion, get_versions)
