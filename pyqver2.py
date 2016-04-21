#!/usr/bin/env python

# Note to devs: Keep backwards compatibility with Python 2.3.

import compiler
import platform
import re
import sys
#from pyqverbase import run, Printer
from pyqver import pyqverbase

DefaultMinVersion = (2, 3)

Py2StandardModules = {
    "__future__":       (2, 1),
    "abc":              (2, 6),
    "argparse":         (2, 7),
    "ast":              (2, 6),
    "atexit":           (2, 0),
    "bz2":              (2, 3),
    "cgitb":            (2, 2),
    "collections":      (2, 4),
    "contextlib":       (2, 5),
    "cookielib":        (2, 4),
    "cProfile":         (2, 5),
    "csv":              (2, 3),
    "ctypes":           (2, 5),
    "datetime":         (2, 3),
    "decimal":          (2, 4),
    "difflib":          (2, 1),
    "DocXMLRPCServer":  (2, 3),
    "dummy_thread":     (2, 3),
    "dummy_threading":  (2, 3),
    "email":            (2, 2),
    "fractions":        (2, 6),
    "functools":        (2, 5),
    "future_builtins":  (2, 6),
    "hashlib":          (2, 5),
    "heapq":            (2, 3),
    "hmac":             (2, 2),
    "hotshot":          (2, 2),
    "HTMLParser":       (2, 2),
    "importlib":        (2, 7),
    "inspect":          (2, 1),
    "io":               (2, 6),
    "itertools":        (2, 3),
    "json":             (2, 6),
    "logging":          (2, 3),
    "modulefinder":     (2, 3),
    "msilib":           (2, 5),
    "multiprocessing":  (2, 6),
    "netrc":            (1, 5, 2),
    "numbers":          (2, 6),
    "optparse":         (2, 3),
    "ossaudiodev":      (2, 3),
    "pickletools":      (2, 3),
    "pkgutil":          (2, 3),
    "platform":         (2, 3),
    "pydoc":            (2, 1),
    "runpy":            (2, 5),
    "sets":             (2, 3),
    "shlex":            (1, 5, 2),
    "SimpleXMLRPCServer": (2, 2),
    "spwd":             (2, 5),
    "sqlite3":          (2, 5),
    "ssl":              (2, 6),
    "stringprep":       (2, 3),
    "subprocess":       (2, 4),
    "sysconfig":        (2, 7),
    "tarfile":          (2, 3),
    "textwrap":         (2, 3),
    "timeit":           (2, 3),
    "unittest":         (2, 1),
    "uuid":             (2, 5),
    "warnings":         (2, 1),
    "weakref":          (2, 1),
    "winsound":         (1, 5, 2),
    "wsgiref":          (2, 5),
    "xml.dom":          (2, 0),
    "xml.dom.minidom":  (2, 0),
    "xml.dom.pulldom":  (2, 0),
    "xml.etree.ElementTree": (2, 5),
    "xml.parsers.expat":(2, 0),
    "xml.sax":          (2, 0),
    "xml.sax.handler":  (2, 0),
    "xml.sax.saxutils": (2, 0),
    "xml.sax.xmlreader":(2, 0),
    "xmlrpclib":        (2, 2),
    "zipfile":          (1, 6),
    "zipimport":        (2, 3),
    "_ast":             (2, 5),
    "_winreg":          (2, 0),
}

Py3StandardModules = {
#    "argparse":         (3, 2), not in 3.0/3.1, but shrug
    "faulthandler":     (3, 3),
#    "importlib":        (3, 1), also in 2.7
    "ipaddress":        (3, 3),
    "lzma":             (3, 3),
    "tkinter.ttk":      (3, 1),
    "unittest.mock":    (3, 3),
    "venv":             (3, 3),
}

StandardModules = {}
StandardModules.update(Py2StandardModules)
StandardModules.update(Py3StandardModules)


Py2Functions = {
    "all":                      (2, 5),
    "any":                      (2, 5),
    "collections.Counter":      (2, 7),
    "collections.defaultdict":  (2, 5),
    "collections.OrderedDict":  (2, 7),
    "enumerate":                (2, 3),
    "frozenset":                (2, 4),
    "itertools.compress":       (2, 7),
    "logging.config.fileConfig": (2, 6),
    "logging.config.dictConfig": (2, 7),
    "logging.handlers.WatchedFileHandler": (2, 6),
    "logging.NullHandler":      (2, 7),
    "math.erf":                 (2, 7),
    "math.erfc":                (2, 7),
    "math.expm1":               (2, 7),
    "math.gamma":               (2, 7),
    "math.lgamma":              (2, 7),
    "memoryview":               (2, 7),
    "next":                     (2, 6),
    "os.getresgid":             (2, 7),
    "os.getresuid":             (2, 7),
    "os.initgroups":            (2, 7),
    "os.setresgid":             (2, 7),
    "os.setresuid":             (2, 7),
    "reversed":                 (2, 4),
    "set":                      (2, 4),
    "subprocess.check_call":    (2, 5),
    "subprocess.check_output":  (2, 7),
    "sum":                      (2, 3),
    "symtable.is_declared_global": (2, 7),
    "weakref.WeakSet":          (2, 7),
}

# TODO: check docs for backports
# Some of these may have been backported to 2.x

Py3Functions = {
    "bytearray.maketrans":                      (3, 1),
    "bytes.maketrans":                          (3, 1),
    "bz2.open":                                 (3, 3),
    "collections.Counter":                      (3, 1),
    "collections.OrderedDict":                  (3, 1),
    "crypt.mksalt":                             (3, 3),
    "email.generator.BytesGenerator":           (3, 2),
    "email.message_from_binary_file":           (3, 2),
    "email.message_from_bytes":                 (3, 2),
    "functools.lru_cache":                      (3, 2),
    "gzip.compress":                            (3, 2),
    "gzip.decompress":                          (3, 2),
    "inspect.getclosurevars":                   (3, 3),
    "inspect.getgeneratorlocals":               (3, 3),
    "inspect.getgeneratorstate":                (3, 2),
    "itertools.combinations_with_replacement":  (3, 1),
    "itertools.compress":                       (3, 1),
    "logging.config.dictConfig":                (3, 2),
    "logging.NullHandler":                      (3, 1),
    "math.erf":                                 (3, 2),
    "math.erfc":                                (3, 2),
    "math.expm1":                               (3, 2),
    "math.gamma":                               (3, 2),
    "math.isfinite":                            (3, 2),
    "math.lgamma":                              (3, 2),
    "math.log2":                                (3, 3),
    "os.environb":                              (3, 2),
    "os.fsdecode":                              (3, 2),
    "os.fsencode":                              (3, 2),
    "os.fwalk":                                 (3, 3),
    "os.getenvb":                               (3, 2),
    "os.get_exec_path":                         (3, 2),
    "os.getgrouplist":                          (3, 3),
    "os.getpriority":                           (3, 3),
    "os.getresgid":                             (3, 2),
    "os.getresuid":                             (3, 2),
    "os.get_terminal_size":                     (3, 3),
    "os.getxattr":                              (3, 3),
    "os.initgroups":                            (3, 2),
    "os.listxattr":                             (3, 3),
    "os.lockf":                                 (3, 3),
    "os.pipe2":                                 (3, 3),
    "os.posix_fadvise":                         (3, 3),
    "os.posix_fallocate":                       (3, 3),
    "os.pread":                                 (3, 3),
    "os.pwrite":                                (3, 3),
    "os.readv":                                 (3, 3),
    "os.removexattr":                           (3, 3),
    "os.replace":                               (3, 3),
    "os.sched_get_priority_max":                (3, 3),
    "os.sched_get_priority_min":                (3, 3),
    "os.sched_getaffinity":                     (3, 3),
    "os.sched_getparam":                        (3, 3),
    "os.sched_getscheduler":                    (3, 3),
    "os.sched_rr_get_interval":                 (3, 3),
    "os.sched_setaffinity":                     (3, 3),
    "os.sched_setparam":                        (3, 3),
    "os.sched_setscheduler":                    (3, 3),
    "os.sched_yield":                           (3, 3),
    "os.sendfile":                              (3, 3),
    "os.setpriority":                           (3, 3),
    "os.setresgid":                             (3, 2),
    "os.setresuid":                             (3, 2),
    "os.setxattr":                              (3, 3),
    "os.sync":                                  (3, 3),
    "os.truncate":                              (3, 3),
    "os.waitid":                                (3, 3),
    "os.writev":                                (3, 3),
    "shutil.chown":                             (3, 3),
    "shutil.disk_usage":                        (3, 3),
    "shutil.get_archive_formats":               (3, 3),
    "shutil.get_terminal_size":                 (3, 3),
    "shutil.get_unpack_formats":                (3, 3),
    "shutil.make_archive":                      (3, 3),
    "shutil.register_archive_format":           (3, 3),
    "shutil.register_unpack_format":            (3, 3),
    "shutil.unpack_archive":                    (3, 3),
    "shutil.unregister_archive_format":         (3, 3),
    "shutil.unregister_unpack_format":          (3, 3),
    "shutil.which":                             (3, 3),
    "signal.pthread_kill":                      (3, 3),
    "signal.pthread_sigmask":                   (3, 3),
    "signal.sigpending":                        (3, 3),
    "signal.sigtimedwait":                      (3, 3),
    "signal.sigwait":                           (3, 3),
    "signal.sigwaitinfo":                       (3, 3),
    "socket.CMSG_LEN":                          (3, 3),
    "socket.CMSG_SPACE":                        (3, 3),
    "socket.fromshare":                         (3, 3),
    "socket.if_indextoname":                    (3, 3),
    "socket.if_nameindex":                      (3, 3),
    "socket.if_nametoindex":                    (3, 3),
    "socket.sethostname":                       (3, 3),
    "ssl.match_hostname":                       (3, 2),
    "ssl.RAND_bytes":                           (3, 3),
    "ssl.RAND_pseudo_bytes":                    (3, 3),
    "ssl.SSLContext":                           (3, 2),
    "ssl.SSLEOFError":                          (3, 3),
    "ssl.SSLSyscallError":                      (3, 3),
    "ssl.SSLWantReadError":                     (3, 3),
    "ssl.SSLWantWriteError":                    (3, 3),
    "ssl.SSLZeroReturnError":                   (3, 3),
    "stat.filemode":                            (3, 3),
    "textwrap.indent":                          (3, 3),
    "threading.get_ident":                      (3, 3),
    "time.clock_getres":                        (3, 3),
    "time.clock_gettime":                       (3, 3),
    "time.clock_settime":                       (3, 3),
    "time.get_clock_info":                      (3, 3),
    "time.monotonic":                           (3, 3),
    "time.perf_counter":                        (3, 3),
    "time.process_time":                        (3, 3),
    "types.new_class":                          (3, 3),
    "types.prepare_class":                      (3, 3),
}

Functions = {}
Functions.update(Py2Functions)
Functions.update(Py3Functions)

Identifiers = {
    "False":        (2, 2),
    "True":         (2, 2),
}

# regex: [version_tuple, reason]
SyntaxRegexes = {
    "except.*as.*:": [(2, 5), "except Exception as"],
}


# from http://code.activestate.com/recipes/523034-emulate-collectionsdefaultdict/
# since we'd like to run on python2.4 as well
class defaultdict(dict):
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
            not hasattr(default_factory, '__call__')):
            raise TypeError('first argument must be callable')
        dict.__init__(self, *a, **kw)
        self.default_factory = default_factory
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value
    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()
    def copy(self):
        return self.__copy__()
    def __copy__(self):
        return type(self)(self.default_factory, self)
    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))
    def __repr__(self):
        return 'defaultdict(%s, %s)' % (self.default_factory,
                                        dict.__repr__(self))


def uniq(a):
    if len(a) == 0:
        return []
    else:
        return [a[0]] + uniq([x for x in a if x != a[0]])

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
        self.vers[(2,0)] = []
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
            v = Functions.get(name)
            if v is not None:
                self.add(node, v, "%s function" % name)
        self.default(node)
    def visitClass(self, node):
        if node.bases:
            self.add(node, (2,2) , "new-style class")
        for child in node.getChildNodes():
            if isinstance(child, compiler.ast.Decorators):
                # who to blame, the class or the decorator?
                self.add(node, (2,6), "class decorator")
        self.default(node)
    def visitDecorators(self, node):
        for node in node.nodes:
            self.add(node, (2,4), "decorator")
        self.default(node)
    def visitDictComp(self, node):
        self.add(node, (2,7), "dictionary comprehension")
        self.default(node)
    def visitFloorDiv(self, node):
        self.add(node, (2,2), "// operator")
        self.default(node)
    def visitFrom(self, node):
        v = StandardModules.get(node.modname)
        if v is not None:
            self.add(node, v, node.modname)
        for n in node.names:
            name = node.modname + "." + n[0]
            v = Functions.get(name)
            if v is not None:
                self.add(node, v, name)
    def visitFunction(self, node):
        if node.decorators:
            self.add(node, (2,4), "function decorator")
        self.default(node)
    def visitGenExpr(self, node):
        self.add(node, (2,4), "generator expression")
        self.default(node)
    def visitGetattr(self, node):
        if (isinstance(node.expr, compiler.ast.Const)
            and isinstance(node.expr.value, str)
            and node.attrname == "format"):
            self.add(node, (2,6), "string literal .format()")
            if ',' in node.expr.value:
                self.add(node, (2,7), "format specifier for thousand (comma)")
        self.default(node)
    def visitIfExp(self, node):
        self.add(node, (2,5), "inline if expression")
        self.default(node)
    def visitImport(self, node):
        for n in node.names:
            v = StandardModules.get(n[0])
            if v is not None:
                self.add(node, v, n[0])
        self.default(node)
    def visitName(self, node):
        v = Identifiers.get(node.name)
        if v is not None:
            self.add(node, v, node.name)
        self.default(node)
    def visitReturn(self, node):
        self.default(node)
    def visitSet(self, node):
        self.add(node, (2,7), "set literal")
        self.default(node)
    def visitSetComp(self, node):
        self.add(node, (2,7), "set comprehension")
        self.default(node)
    def visitTryFinally(self, node):
        # try/finally with a suite generates a Stmt node as the body,
        # but try/except/finally generates a TryExcept as the body
        if isinstance(node.body, compiler.ast.TryExcept):
            self.add(node, (2,5), "try/except/finally")
        self.default(node)
    def visitWith(self, node):
        if isinstance(node.body, compiler.ast.With):
            self.add(node, (2,7), "with statement with multiple contexts")
        else:
            self.add(node, (2,5), "with statement")
        self.default(node)
    def visitYield(self, node):
        self.add(node, (2,2), "yield expression")
        self.default(node)


def compile_re():
    compiled = {}
    for regex_string, version_info in SyntaxRegexes.items():
        compiled[re.compile(regex_string)] = version_info
    return compiled
CompiledSyntaxRegexes = compile_re()


# simple checker per line regex
# the only case I know that NodeChecker can't find
# is "except Exception as Foo:", so one line checks are ok
# we may need multiline regexes for some stuff, like f(a,*b,kw='c')
# that are likely to span lines
#
# the regex and/or string match is kind of ugly compared
# to use the parsed tree, but it seems reasonably fast
# and could potentially catch some things that cause
# syntax errors yet parse into the same tree
class LineChecker(object):
    def __init__(self, source):
        self.vers = defaultdict(list)
        self.vers[(2, 0)].append(None)
        self.check(source)

    def check(self, source):
        lines = source.splitlines()
        lineno = 1
        for line in lines:
            for regex, version_info  in CompiledSyntaxRegexes.items():
                if regex.match(line):
                    self.vers[version_info[0]].append((lineno, version_info[1]))


def get_versions(source, filename=None):
    """Return information about the Python versions required for specific features.

    The return value is a dictionary with keys as a version number as a tuple
    (for example Python 2.6 is (2,6)) and the value are a list of features that
    require the indicated Python version.
    """
    tree = compiler.parse(source)
    checker = compiler.walk(tree, NodeChecker())
    line_checker = LineChecker(source)
    checker.vers.update(line_checker.vers)
    return checker.vers

def v27(source):
    if sys.version_info >= (2, 7):
        return qver(source)
    else:
        print >>sys.stderr, "Not all features tested, run --test with Python 2.7"
        return (2, 7)

def qver(source):
    """Return the minimum Python version required to run a particular bit of code.

    >>> qver('print "hello world"')
    (2, 0)
    >>> qver('class test(object): pass')
    (2, 2)
    >>> qver('yield 1')
    (2, 2)
    >>> qver('a // b')
    (2, 2)
    >>> qver('True')
    (2, 2)
    >>> qver('enumerate(a)')
    (2, 3)
    >>> qver('total = sum')
    (2, 0)
    >>> qver('sum(a)')
    (2, 3)
    >>> qver('(x*x for x in range(5))')
    (2, 4)
    >>> qver('class C:\\n @classmethod\\n def m(): pass')
    (2, 4)
    >>> qver('y if x else z')
    (2, 5)
    >>> qver('import hashlib')
    (2, 5)
    >>> qver('from hashlib import md5')
    (2, 5)
    >>> qver('import xml.etree.ElementTree')
    (2, 5)
    >>> qver('try:\\n try: pass;\\n except: pass;\\nfinally: pass')
    (2, 0)
    >>> qver('try: pass;\\nexcept: pass;\\nfinally: pass')
    (2, 5)
    >>> qver('from __future__ import with_statement\\nwith x: pass')
    (2, 5)
    >>> qver('collections.defaultdict(list)')
    (2, 5)
    >>> qver('from collections import defaultdict')
    (2, 5)
    >>> qver('"{0}".format(0)')
    (2, 6)
    >>> qver('memoryview(x)')
    (2, 7)
    >>> v27('{1, 2, 3}')
    (2, 7)
    >>> v27('{x for x in s}')
    (2, 7)
    >>> v27('{x: y for x in s}')
    (2, 7)
    >>> qver('from __future__ import with_statement\\nwith x:\\n with y: pass')
    (2, 5)
    >>> v27('from __future__ import with_statement\\nwith x, y: pass')
    (2, 7)
    >>> qver('@decorator\\ndef f(): pass')
    (2, 4)
    >>> qver('@decorator\\nclass test:\\n pass')
    (2, 6)

    #>>> qver('0o0')
    #(2, 6)
    #>>> qver('@foo\\nclass C: pass')
    #(2, 6)
    """
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

if __name__ == '__main__':
    main()
