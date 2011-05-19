import argparse
import zipfile
import os
import shutil
import logging
import struct
import M2Crypto
import io
import subprocess

log = logging.getLogger(__name__)

class CrxMakeException(Exception):
    pass

def _generate_pem(pem_path):
    key = M2Crypto.RSA.gen_key(1024, 65537, lambda:None)
    pem = key.as_pem(cipher=None)
    fp = open(pem_path, 'w')
    fp.write(pem)
    fp.close()

def _get_der(pem_path):
    return subprocess.Popen(["openssl", "rsa", "-pubout", "-outform", "DER",
        "-inform", "PEM", "-in", pem_path], stdout=subprocess.PIPE)\
        .stdout.read()

def _load_key(path):
    fp = open(path, "r")
    data = fp.read()
    fp.close()
    return data


def _build_zip(zip_buffer, source, ignore_func):
    pathnames = os.listdir(source)
    ignored_pathnames = ignore_func(source, pathnames)
    for pathname in pathnames:
        if pathname in ignored_pathnames:
            log.info("Ignoring %s" % (pathname))
            continue

        full_path = os.path.join(source, pathname)
        if os.path.isdir(full_path):
            _build_zip(zip_buffer, full_path, ignore_func)
        elif os.path.isfile(full_path):
            log.info('Adding %s' % full_path)
            zip_buffer.write(full_path)
        
    return zip_buffer


def _pack_zip(source, output, ignore, close=False):
    z = zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED)
    ignores = ignore.split(',')
    if isinstance(output, basestring):
        ignores.extend([output])
    ignore_func = shutil.ignore_patterns(*ignores)
    _build_zip(z, source, ignore_func)
    
    if close:
        z.close()

    return z

def make_crx(source, output, ignore, key=None):
    if not os.path.exists(source):
        raise CrxMakeException('Source directory %s does not exist' % source)
    
    if not key:
        key = 'extension.pem'
        _generate_pem(key)

    logging.info('Making crx from %s' % source)

    out = io.BytesIO()
    _pack_zip(source, out, ignore, close=False)

    pkey = M2Crypto.EVP.load_key_string(_load_key(key))
    pkey.sign_init()
    pkey.sign_update(out.getvalue())
    sign = pkey.sign_final()

    der_key = _get_der(key)
    

    magic = "Cr24"
    version = struct.pack("<I", 2)
    key_len = struct.pack("<I", len(der_key))
    sign_len = struct.pack("<I", len(sign))

    fp = open(output, "w")
    fp.write(magic)
    fp.write(version)
    fp.write(key_len)
    fp.write(sign_len)
    fp.write(der_key)
    fp.write(sign)
    fp.write(out.getvalue())
    fp.flush()

    fp.close()


    return 0
    
def make_zip(source, output, ignore):
    if not os.path.exists(source):
        raise CrxMakeException('Source directory %s does not exist' % source)
    
    logging.info('Making zip from %s' % source)
    _pack_zip(source, output, ignore, close=True)
    log.info('Zip written to %s' % output)
    return 0



def main():
    def _error(msg, parser):
        print "Error: %s" % msg
        parser.print_help()
        return -1

    parser = argparse.ArgumentParser(description='Build tools for chrome extensions.')
    parser.add_argument('-s', '--source', dest='source', default='.', help="Source path")
    parser.add_argument('-m', '--mode', dest='mode', default='crx', help="Build a CRX or ZIP")
    parser.add_argument('-o', '--output', dest='output', required=True, help="Output path")
    parser.add_argument('-k', '--key', dest='key', help="Path to key file")
    parser.add_argument('-i', '--ignore', dest='ignore', default="*.py,.git/",  help="Ignore")

    args = parser.parse_args()

    if args.mode == 'crx':
        try:
            return make_crx(args.source, args.output, args.ignore, args.key)
        except CrxMakeException, e:
            return _error(e, parser)

    elif args.mode == 'zip':
        try:
            return make_zip(args.source, args.output, args.ignore)
        except CrxMakeException, e:
            return _error(e, parser)
    else:
        return _error("Invalid mode %s specified." % args.mode, parser)



if __name__ == '__main__':
    main()

