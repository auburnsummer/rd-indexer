from typing import BinaryIO
from zipfile import ZipFile
from orchard.vitals.arguments_decorator import with_arguments

import hashlib

# BUF_SIZE is totally arbitrary, change for your app!

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!


@with_arguments("file")
def sha1_facet(f: BinaryIO):
    return _sha1(f)


def _sha1(f: BinaryIO):
    sha1 = hashlib.sha1()
    f.seek(0)
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        sha1.update(data)
    return sha1.hexdigest()
