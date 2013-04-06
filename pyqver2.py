#!/usr/bin/env python

import compiler
import platform
import pprint
pp = pprint.pprint
import sys
from collections import deque

try:
    import ast
    from ast import iter_child_nodes
except ImportError:
    from flake8.util import ast, iter_child_nodes

StandardModules = {
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

Functions = {
    "all":                      (2, 5),
    "any":                      (2, 5),
    "collections.Counter":      (2, 7),
    "collections.defaultdict":  (2, 5),
    "collections.OrderedDict":  (2, 7),
    "enumerate":                (2, 3),
    "frozenset":                (2, 4),
    "itertools.compress":       (2, 7),
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
    "sum":                      (2, 3),
    "symtable.is_declared_global": (2, 7),
    "weakref.WeakSet":          (2, 7),
}

Identifiers = {
    "False":        (2, 2),
    "True":         (2, 2),
}


def uniq(a):
    if len(a) == 0:
        return []
    else:
        return [a[0]] + uniq([x for x in a if x != a[0]])


class NodeChecker(ast.NodeVisitor):
    def __init__(self):
        #self.visitors = BaseASTCheck._checks
        self.vers = dict()
        self.vers[(2, 0)] = []
        self.parents = deque()

    def check_ver(self, ver):
        #if ver not in self.vers:
        #    self.vers[ver] = []
        #self.vers[ver].append((node.lineno, msg))
        if ver >= (2,2):
            return True
        return False

#    def default(self, node):
#        print node, dir(node)
#        for child in node.getChildNodes():
#            self.visit(child)

    def _err(self, node, ver, code):
        print "err", node, ver, code
        if hasattr(node, 'lineno'):
            lineno, col_offset = node.lineno, node.col_offset
        if isinstance(node, ast.keyword):
            lineno = node.value.lineno
            col_offset = node.value.col_offset
        if isinstance(node, ast.ClassDef):
            lineno += len(node.decorator_list)
            col_offset += 6
        elif isinstance(node, ast.FunctionDef):
            lineno += len(node.decorator_list)
            col_offset += 4
        msg =  '%s  %s %s' % (code, ver, getattr(self, code))
        print lineno, col_offset, msg, self
        return (lineno, col_offset, msg, self)

    def visit_tree(self, node):
        print "__"*len(self.parents), "visit_tree: ", node
        for error in self.visit_node(node):
            yield error
        self.parents.append(node)
        for child in iter_child_nodes(node):
            for error in self.visit_tree(child):
                yield error
        self.parents.pop()

    def visit_node(self, node):
        indent = " "*len(self.parents)
        #pp(node._fields)
        for field in node._fields:
            print indent, "%s:%s" % (field, getattr(node, field))
        if node:
            method = 'visit' + node.__class__.__name__
            print "method", method, hasattr(self, method)
            if hasattr(self, method):
                #continue
                print "VISTOR FOR: ", method
                yield getattr(self, method)(node)
        else:
            print "method no attr", method
            yield self.visit_tree(node)


    default = visit_tree

    def visitImportFrom(self, node):
        print "ImportFrom:", node
        #self.visit_tree(node)
        self.V801 = 'I dont like import from'
        foo = self._err(node, (2,3), 'V801')
        print "foo", foo
        return foo
        #yield (1,2,3,4)
#        yield iter_child_nodes(node)
        self.visit_tree(node)

    def visitkeyword(self, node):
        for child in iter_child_nodes(node):
            self.generic_visit(child)

        print "keyword", node
        self.V802 = "keywords!!!!!!!"
        arg = node.arg
        value = node.value
        print "arg: ", arg, "value: ", value
        return self._err(node, (2,3), 'V802')
#        if arg == 'name':
#            return self._err(node, (2,3), 'V802')
#        self.visit_tree(node)
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
                if self.check_ver(v):
                    return self.err(node, v, 'V801')
                #self.add(node, v, name)
        self.visit_node(node)

    def visitClass(self, node):
        if node.bases:
            if self.check_ver((2, 2)):
                return self.err(node, (2,2), "new-style class")
        if node.decorators:
            if self.check_ver((2,6)):
                return self.err(node, (2,6), "class decorator")
        self.visit_node(node)

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

    def visit_blip_Name(self, node):
        print "node.id", node.id, node.ctx
        v = Identifiers.get(node.id)
        if v is not None:
            if self.check_ver(v):
                yield self.err(node, v, node.id)
        yield self.visit_tree(node)

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

def get_versions(source):
    """Return information about the Python versions required for specific features.

    The return value is a dictionary with keys as a version number as a tuple
    (for example Python 2.6 is (2,6)) and the value are a list of features that
    require the indicated Python version.
    """
    tree = compiler.parse(source)
    checker = compiler.walk(tree, NodeChecker())
    return checker.vers

def check_file(filename):
    print "cf", filename
    f = open(filename, 'r')
    buf = f.read()
    f.close()
    return get_versions(buf)

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


def main():
    Verbose = False
    MinVersion = (2, 3)
    Lint = False

    files = []
    i = 1
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--test":
            import doctest
            doctest.testmod()
            return 0
        if a == "-v" or a == "--verbose":
                Verbose = True
        elif a == "-l" or a == "--lint":
            Lint = True
        elif a == "-m" or a == "--min-version":
            i += 1
            MinVersion = tuple(map(int, sys.argv[i].split(".")))
        else:
            files.append(a)
        i += 1

    if not files:
        print >>sys.stderr, """Usage: %s [options] source ...

        Report minimum Python version required to run given source files.

        -m x.y or --min-version x.y (default 2.3)
            report version triggers at or above version x.y in verbose mode
        -v or --verbose
            print more detailed report of version triggers for each version
    """ % sys.argv[0]
        return 1

    check_files(files, MinVersion)

def check_files(files, MinVersion, Verbose=False, Lint=False):
    for fn in files:
        try:
            ver = check_file(fn)
            if Verbose:
                print fn
                for v in sorted([k for k in ver.keys() if k >= MinVersion], reverse=True):
                    reasons = [x for x in uniq(ver[v]) if x]
                    if reasons:
                        # each reason is (lineno, message)
                        print "\t%s\t%s" % (".".join(map(str, v)), ", ".join([x[1] for x in reasons]))
            elif Lint:
                for v in sorted([k for k in ver.keys() if k >= MinVersion], reverse=True):
                    reasons = [x for x in uniq(ver[v]) if x]
                    for r in reasons:
                        # each reason is (lineno, message)
                        print "%s:%s: %s %s" % (fn, r[0], ".".join(map(str, v)), r[1])
            else:
                print "%s\t%s" % (".".join(map(str, max(ver.keys()))), fn)
        except SyntaxError, x:
            print "%s: syntax error compiling with Python %s: %s" % (fn, platform.python_version(), x)


class PyqverChecker(object):
    name = "pyqver"
    version = "1.0"
    min_python_version = (2, 2)

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.min_version = (2, 4)
        print "tree", tree
        print "filename", filename

    def run(self):
        # FIXME: should be iterator based on when tree walk hits a version
        # mismatch
        return self.check_tree()
        #print "iter", iter, dir(iter)
        #return iter

    def check_tree(self):
        checker = NodeChecker()
        return checker.visit_tree(self.tree)
        #import pprint
        #pprint.pprint(checker.vers)

    def check_file(self, filename):
        ver = check_file(self.filename)
        all_errors = []
        for v in sorted([k for k in ver.keys() if k >= self.min_python_version],
                        reverse=True):
            reasons = [x for x in uniq(ver[v]) if x]
            for r in reasons:
                # lineno, offset, text, check
                # note we dont compute offset
                msg = "[%s] %s" % (".".join(map(str, v)), r[1])
                all_errors.append((r[0],
                                   0,
                                   # heh, some non obvious string escaping
                                   # here
                                   msg,
                                   #"%s %s" % (msg, r[1]),
                                   '80'))
        return iter(all_errors)

    @classmethod
    def add_options(cls, parser):
        parser.add_option("--min-python-version", default="2.2",
                          action="store", dest="min_python_version",
                          help="oldest version of python to support")
        parser.config_options.append("min-python-version")

    @classmethod
    def parser_options(cls, options):
        cls.min_python_version = tuple(map(int, options.min_python_version.split(".")))


if __name__ == "__main__":
    sys.exit(main())
