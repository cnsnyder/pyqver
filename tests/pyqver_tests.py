
# multiple with statement (2, 7(
# from __future__ import with_statement

try:
    import argparse
except ImportError, e:
    pass

try:
    import argparse
except (ImportError, KeyError) as e:
    pass

try:
    import argparse
except ImportError as e:
    pass
finally:
    print 'pass'

print "hello world"  # 2.0

# nested try/except/finally ok for (2, 0)
try:
    try:
        pass
    except:
        pass
finally:
    pass


# new style classes
class test(object):
    pass  # (2, 2)


# yield statement
def yielder():
    for x in [1, 2, 3]:
        yield 1  # (2.2)

# yes, lets add a fundamental type in a .2
print True  # (2, 2)


a = 4
b = 9
c = 8
a = 100 + c // b - 1

# floordiv
print a // b  # (2, 2)

a_list = [12.3, 4, 4.0]
# enumerate
enumerate(a_list)  # (2, 3)

sum(a_list)  # (2, 3)

# comprenension
(x * x for x in range(5))   # (2, 4)


# @classmethod
class C:
    @classmethod  # (2,4)
    def m():
        pass


rev = reversed([1, 2, 3, 4])  # (2, 4)

import subprocess
a = subprocess.check_output(['ls'])

x = 0
z = False
y if x else z  # (2,5)

# hashlib
import hashlib  # (2, 5)


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


class cm(object):
    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

# future with statement (2, 5)
with cm():
    pass

# ssl in 2.6
import ssl   # (2,6)

# WatchedFileHandler added in 2.6
try:
    from logging.handlers import WatchedFileHandler
except ImportError:
    raise

# new 2.7 modules
try:
    # argparse in 2.7
    import argparse as not_optparse # (2.7)

    # collections.Counter new in 2.7
    from collections import Counter

    # collections.OrderedDict new in 2.7
    from collections import OrderedDict

    # NullHandler added in 2.7
    from logging import NullHandler
    import logging
    foo = logging.NullHandler
except ImportError:
    pass

# pep 378, ',' format specifier for thousans
foo = '{:20,.2f}'.format(18446744073709551616.0)
bar = '{:20,d}'.format(18446744073709551616)

blip = '{0},{1}'.format('sdfadf', 'sfsdfsdfserer')

# multiple with statement (2, 7(
with cm():
    pass
    with cm():    # (2, 5)
        pass
    pass

# some py3+ modules
try:
    import faulthandler   # (3,3)
    import ipaddress      # (3,3)
    import lzma
    import tkinter.ttk
    import unittest.mock
    import venv
except ImportError as e:
    print e

# some py3 functions

try:
    import bz2
    f = bz2.open('/sdfd')
except Exception as e:
    print e

"""
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
