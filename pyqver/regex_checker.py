import re

from pyqver.compat import defaultdict as compat_defaultdict

# regex: [version_tuple, reason]
SyntaxRegexes = {
    "except.*as.*:": [(2, 5), "except Exception as"],
}


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
        self.vers = compat_defaultdict.defaultdict(list)
        self.vers[(2, 0)].append(None)
        self.check(source)

    def check(self, source):
        lines = source.splitlines()
        for lineno, line in enumerate(lines, 1):
            for regex, version_info in CompiledSyntaxRegexes.items():
                if regex.match(line):
                    self.vers[version_info[0]].append((lineno, version_info[1]))
