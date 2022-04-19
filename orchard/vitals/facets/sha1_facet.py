from typing import BinaryIO
from zipfile import ZipFile

import hashlib

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

sha1 = hashlib.sha1()


def sha1_facet(obj, z: ZipFile, f: BinaryIO):
    f.seek(0)
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        sha1.update(data)
    return sha1.hexdigest()