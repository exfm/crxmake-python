# crxmake-python

Python tools for chrome extensions.

* Build standalone signed CRX files
* Build zip files to upload to the gallery
* Generate keys

It is inspired by rubygems' crxmake.

## Usage:

    crxmake.py PACKAGE_BASE_DIR

## Requires:

- python 2
- M2Crypto
- "openssl" command: because current M2Crypto lacks func for rsa pubout DER

## Resources:

- "M2Crypto":http://chandlerproject.org/bin/view/Projects/MeTooCrypto
- "crxmake":http://github.com/Constellation/crxmake
- "Packing Chrome extensions in Python":http://grack.com/blog/2009/11/09/packing-chrome-extensions-in-python/
