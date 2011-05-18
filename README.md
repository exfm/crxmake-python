# crxmake-python

Python tools for chrome extensions.

* Build standalone signed CRX files
* Build zip files to upload to the gallery
* Generate keys

It is inspired by rubygems' crxmake.

## Usage
    
### Package a signed CRX for distribution

    crxmake -o <extension-name>.crx -k <pem-path> -i <comma-sep-ignore-patterns>

### Package a zip for uploading to the gallery

    crxmake -o <extension-name>.zip -m zip -i <comma-sep-ignore-patterns>
    
## Requirements

* "openssl" command: because current M2Crypto lacks func for rsa pubout DER

## Resources

* (M2Crypto)[http://chandlerproject.org/bin/view/Projects/MeTooCrypto]
* (Ruby crxmake)[http://github.com/Constellation/crxmake]
* (Packing Chrome extensions in Python)(http://grack.com/blog/2009/11/09/packing-chrome-extensions-in-python)