from datetime import datetime
import json
import sys
from math import floor

import httpx
from sqlite_utils import Database
import itertools

from orchard.bot.constants import DEFAULT_DB_VALUE
from orchard.bot.schema import STATUS_SCHEMA
from orchard.scan.schema import LEVEL_SCHEMA

COMBINED_SCHEMA = {
    **LEVEL_SCHEMA,
    **STATUS_SCHEMA
}


def none_or(func):
    def inner(value):
        if value is None:
            return None
        else:
            return func(value)
    return inner


def make_json_from_row(row):
    type_transformers = {
        bool: lambda n: True if n > 0 else False,
        datetime: none_or(lambda s: floor(datetime.fromisoformat(s).timestamp()))
    }
    key_transformers = {
        "tags": lambda s: json.loads(s),
        "authors": lambda s: json.loads(s),
    }
    for col_name, col_value in row.items():
        col_type = COMBINED_SCHEMA[col_name]
        if col_type in type_transformers.keys():
            row[col_name] = type_transformers[col_type](col_value)
        if col_name in key_transformers.keys():
            row[col_name] = key_transformers[col_name](col_value)

    return row

def prerun_make_combined_db(rows):
    combined = Database("./combined.db")
    combined['levels'].create(COMBINED_SCHEMA, pk='id')
    combined['levels'].insert_all(rows)


def package(db: Database, status_db: Database):
    # map status id to the rest of the object.
    statuses = { r['id']: {k: v for k, v in r.items() if k != 'id'} for r in status_db['status'].rows }
    combined = []
    for row in db['level'].rows:
        id = row['id']
        status = statuses[id] if id in statuses else {}
        combined.append({
            **row,
            **DEFAULT_DB_VALUE,
            **status
        })

    prerun_make_combined_db(combined)

    with open("./orchard.jsonl", "w") as f:
        for row in combined:
            processed = make_json_from_row(row)
            s = json.dumps(processed)
            f.write(s + "\n")


if __name__ == "__main__":
    file = sys.argv[1]
    status_file = sys.argv[2]
    package(Database(file), Database(status_file))
