from zipfile import ZipFile
from datetime import datetime

from orchard.vitals.arguments_decorator import with_arguments


@with_arguments("zip")
def updated_facet(zip):
    info = zip.getinfo("main.rdlevel")
    return datetime(*info.date_time)
