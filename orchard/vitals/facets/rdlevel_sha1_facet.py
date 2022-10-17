# this is the sha1 of the .rdlevel file.
# this may be used for third party integrations as an easier way to determine "is this level already installed locally"
import hashlib
from zipfile import ZipFile

from orchard.vitals.arguments_decorator import with_arguments

sha1 = hashlib.sha1()


@with_arguments("zip")
def rdlevel_sha1_facet(z: ZipFile):
    with z.open("main.rdlevel") as rdlevel:
        text = rdlevel.read()
        sha1.update(text)
    return sha1.hexdigest()