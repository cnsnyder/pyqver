#!/usr/bin/python

from setuptools import setup
from setuptools import find_packages

setup(name="pyqver",
      version='1.3',
      url="https://github.com/alikins/pyqver",
      description="Identify the minimum Python version required for a given script.",
      author="Greg Hewgill, Adrian Likins",
      packages=find_packages(),
      scripts=['pyqver3.py'],
      entry_points={'console_scripts':
                    ['pyqver2 = pyqver.pyqver2:main'],
                    'flake8.extension':
                    ['pyqver = pyqver.checker:PyqverChecker']}
      )
