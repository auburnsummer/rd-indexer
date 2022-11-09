from datetime import datetime
import json
import sys
from math import floor

from playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import SqliteExtDatabase

from orchard.bot.lib.constants import DEFAULT_DB_STATUS_VALUE
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

    def default_step(col_name, col_value, final_dict):
        final_dict[col_name] = col_value
        return final_dict

    def with_func(func):
        def inner(col_name, col_value, final_dict):
            final_dict[col_name] = func(col_value)
            return final_dict
        return inner

    def source_metadata_step(col_name, col_value, final_dict):
        if col_value is None:
            return final_dict
        final_dict["discord_metadata__user_id"] = col_value["user_id"]
        final_dict["discord_metadata__timestamp"] = col_value["timestamp"]
        return final_dict
        
    # dict of keys to functions that do stuff with the value.
    # we run through the functions to build a final object which then gets JSON serialised into the jsonl.
    steps = {
        "last_updated": with_func(datetime_to_epoch),
        "indexed": with_func(datetime_to_epoch),
        "song_ct": with_func(json.dumps),
        "description_ct": with_func(json.dumps),
        "source_metadata": source_metadata_step
    }

    final_dict = {}
    for col_name, col_value in combined_dict.items():
        step = steps[col_name] if col_name in steps else default_step
        final_dict = step(col_name, col_value, final_dict)

    return json.dumps(final_dict, ensure_ascii=False)


def package():
    # create the combined db.
    combined = SqliteExtDatabase("./combined.db")
    Combined.bind(combined)
    combined.create_tables([Combined])

    # populate the combined db.
    for row in Level.select():
        status, _ = Status.get_or_create(id=row.id, defaults=DEFAULT_DB_STATUS_VALUE)
        print(row)
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
