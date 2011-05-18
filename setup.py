#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "crxmake",
      version = '0.1',
      description = "Tools for Chrome Extensions",
      author = "Lucas Hrabovsky",
      author_email = "lucas@ex.fm",
      scripts = [],
      install_requires=['M2Crypto'],
      url = "http://github.com/exfm/crxmake-python",
      packages = [],
      license = 'BSD'
)