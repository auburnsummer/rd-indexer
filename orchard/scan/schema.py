# Given an empty db, create a schema for it.
from playhouse.sqlite_ext import SqliteExtDatabase
from sqlite_utils import Database
import datetime

from sqlite_utils.db import NotFoundError

from orchard.db.models import Level

LEVEL_SCHEMA = {
    "id": str,
    "artist": str,
    "artist_tokens": str,
    "song": str,
    "seizure_warning": bool,
    "description": str,
    "hue": float,
    "authors": str,
    "max_bpm": float,
    "min_bpm": float,
    "difficulty": int,
    "single_player": bool,
    "two_player": bool,
    "last_updated": datetime.datetime,  # alias to string
    "tags": str,
    "thumb": str,
    "image": str,
    "url": str,
    "url2": str,
    "icon": str,
    "has_classics": bool,
    "has_oneshots": bool,
    "has_squareshots": bool,
    "has_freezeshots": bool,
    "has_freetimes": bool,
    "has_skipshots": bool,
    "has_holds": bool,
    "has_window_dance": bool,
    "source": str,
    "source_iid": str,
    "sha1": str
}


def make_schema(db: Database):

    db["level"].create(
        LEVEL_SCHEMA,
        pk="id",
        not_null=set(LEVEL_SCHEMA.keys()) - {"thumb, url, icon"},
    )


class OrchardDatabase:
    def __init__(self, db: SqliteExtDatabase):
        self.db = db

    def add_level(self, level):
        self.db["level"].insert(level, pk="id")

    def delete_level(self, source_id, source_iid):
        iter = self.db["level"].rows_where(
            "source = ? AND source_iid = ?", [source_id, source_iid]
        )
        iter = list(iter)
        if iter:
            row = iter[0]
            self.db["level"].delete(row["id"])

    def does_level_exist(self, id):
        try:
            self.db["level"].get(id)
            return True
        except NotFoundError:
            return False

    def get_source_set(self, source_id):
        return set(row.source_iid for row in Level.select().where(Level.source == source_id))
        # return set(
        #     r["source_iid"]
        #     for r in self.db["level"].rows_where("source = ?", [source_id])
        # )
