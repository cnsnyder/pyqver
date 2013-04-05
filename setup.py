
from setuptools import setup

setup(name="pyqver",
      version="1.0",
      description=" identify the minimum version of Python that is required to execute a particular source file",
      py_modules=["pyqver2"],
      entry_points={'flake8.extension': ['V80 = pyqver2:PyqverChecker']}
      )
