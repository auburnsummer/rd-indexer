from sqlite_utils import Database
from sqlite_utils.db import NotFoundError


def get_or_default(db: Database, id):
    try:
        db['status'].get(id)
    except NotFoundError:
        db['status'].insert({
            "id": id,
            "approval": 0,
        })
    finally:
        return db['status'].get(id)