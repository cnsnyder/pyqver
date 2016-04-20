print "hello world"  # 2.0

# new style classes
class test(object):
    pass  # (2, 2)


# yield statement
def yielder():
    for x in [1, 2, 3]:
        yield 1  # (2.2)

# floordiv
print a // b  # (2, 2)

b = 9
c = 8
a = 100 + c // b - 1
print True  # (2, 2)

# enumerate
enumerate(a)  # (2, 3)

sum(a)  # (2, 3)

# comprenension
(x * x for x in range(5))   # (2, 4)

# @classmethod
class C:
    @classmethod  # (2,4)
    def m():
        pass

y if x else z  # (2,5)

# hashlib
import hashlib  # (2, 5)

# ssl in 2.6
import ssl   # (2,6)

# argparse in 2.7
import argparse as not_optparse # (2.7)

from hashlib import md5  # (2,5)

# ElementTree
import xml.etree.ElementTree  # (2,5)

# try/finally  # 2.5?
try:
    pass
except:
    pass
finally:
    pass

# nested try/except/finally ok for (2, 0)
try:
    try:
        pass
    except:
        pass
finally:
    pass

# future with statement (2, 5)
from __future__ import with_statement
with x:
    pass

# multiple with statement (2, 7(
from __future__ import with_statement
with x:
    pass
    with y:    # (2, 5)
        pass
    pass
"""
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
    "
"""
