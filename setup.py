#!/usr/bin/env python

from setuptools import setup
setup(
    name='crxmake-python',
    version='0.1',
    url='http://ex.fm/',
    license='BSD',
    author='Lucas Hrabovsky',
    author_email='lucas@ex.fm',
    description='Tools for Chrome Extensions',
    zip_safe=False,
    install_requires=[
        'M2Crypto'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License'
    ],
    entry_points = {
        'console_scripts': [
            'crxmake = crxmake:main'
        ],
    }
)