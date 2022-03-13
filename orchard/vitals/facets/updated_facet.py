from zipfile import ZipFile
from datetime import datetime


def updated_facet(_, zip: ZipFile):
    info = zip.getinfo("main.rdlevel")
    return datetime(*info.date_time)