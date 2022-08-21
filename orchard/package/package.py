from datetime import datetime
import json
import sys
from math import floor

from playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import SqliteExtDatabase

from orchard.bot.constants import DEFAULT_DB_STATUS_VALUE
from orchard.db.models import Level, Status, Combined


def make_jsonl_from_combined(combined):
    combined_dict = model_to_dict(combined)

    def datetime_to_epoch(s):
        if s is None:
            return None
        if isinstance(s, str):
            return floor(datetime.fromisoformat(s).timestamp())
        if isinstance(s, datetime):
            return floor(s.timestamp())
        return None
    # dict of keys to functions that transform the value.
    transformers = {
        "last_updated": datetime_to_epoch,
        "indexed": datetime_to_epoch
    }
    for col_name, col_value in combined_dict.items():
        if col_name in transformers.keys():
            combined_dict[col_name] = transformers[col_name](col_value)

    return json.dumps(combined_dict, ensure_ascii=False)


def package():
    # create the combined db.
    combined = SqliteExtDatabase("./combined.db")
    Combined.bind(combined)
    combined.create_tables([Combined])

    # populate the combined db.
    for row in Level.select():
        status, _ = Status.get_or_create(id=row.id, defaults=DEFAULT_DB_STATUS_VALUE)
        print(row)
        print(status)
        to_insert = {
            **model_to_dict(row),
            **model_to_dict(status)
        }
        Combined.create(**to_insert)

    # produce a jsonlines file for typesense.
    with open("./orchard.jsonl", "w") as f:
        for row in Combined.select():
            f.write(make_jsonl_from_combined(row) + "\n")


if __name__ == "__main__":
    file = sys.argv[1]
    status_file = sys.argv[2]

    db1 = SqliteExtDatabase(file)
    db2 = SqliteExtDatabase(status_file)
    Level.bind(db1)
    Status.bind(db2)
    package()
