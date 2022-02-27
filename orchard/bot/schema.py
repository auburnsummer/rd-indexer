import datetime

from sqlite_utils import Database

STATUS_SCHEMA = {
    "id": str,
    "approval": int,
    "approval_reasons": str,
    "indexed": datetime.datetime,  # when it was first approved, or null otherwise.
}


def make_schema(db: Database):
    db["status"].create(
        STATUS_SCHEMA,
        pk="id",
    )
