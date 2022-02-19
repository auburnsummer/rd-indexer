import datetime

from sqlite_utils import Database

STATUS_SCHEMA = {
    "id": str,
    "approval": int,
    "approval_reasons": str,
    "indexed": datetime.datetime
}

def make_schema(db: Database):
    db["level"].create(
        STATUS_SCHEMA,
        pk="id",
    )