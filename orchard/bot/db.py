from sqlite_utils import Database
from sqlite_utils.db import NotFoundError

from orchard.bot.constants import DEFAULT_DB_VALUE


def get_or_default(db: Database, id, default_approval):
    try:
        db["status"].get(id)
    except NotFoundError:
        db["status"].insert({"id": id, "approval": default_approval})
    finally:
        return db["status"].get(id)


def set_status(db: Database, id, value):
    get_or_default(db, id, 0)  # ensure it exists
    db["status"].update(id, value)