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
from orchard.scan.sources.old_sheet import SHEET_API_URL


def none_or(func):
    def inner(value):
        if value is None:
            return None
        else:
            return func(value)
    return inner


def make_json_from_row(row):
    combined_schema = {
        **LEVEL_SCHEMA,
        **STATUS_SCHEMA
    }
    type_transformers = {
        bool: lambda n: True if n > 0 else False,
        datetime: none_or(lambda s: floor(datetime.fromisoformat(s).timestamp()))
    }
    key_transformers = {
        "tags": lambda s: json.loads(s),
        "authors": lambda s: json.loads(s),
    }
    for col_name, col_value in row.items():
        col_type = combined_schema[col_name]
        if col_type in type_transformers.keys():
            row[col_name] = type_transformers[col_type](col_value)
        if col_name in key_transformers.keys():
            row[col_name] = key_transformers[col_name](col_value)

    return row


def prerun_import_oldsheet(db: Database, status_db: Database):
    resp = httpx.get(SHEET_API_URL, follow_redirects=True)
    resp_json = resp.json()
    iids = [(x['download_url'], x['verified']) for x in resp_json if 'verified' in x]
    for (iid, will_approve) in iids:
        level_row = list(db['level'].rows_where("source_iid = :iid", {'iid': iid}))
        if level_row:
            level_row = level_row[0]
            id = level_row['id']
            # rules: if it has gone from (-1 | 0) -> 10, update the index.
            to_upsert = {
                'id': id,
                'approval': 10 if will_approve else -1,
            }
            status_db['status'].upsert(to_upsert, pk='id')

def prerun_update_indexed_column(db: Database, status_db: Database):

    approved_rows = status_db['status'].rows_where("approval >= 10")
    time = datetime.now()
    for row in approved_rows:
        indexed = row['indexed']
        if indexed is None:
            status_db['status'].upsert({
                'id': row['id'],
                'indexed': time,
            }, pk='id')


def package(db: Database, status_db: Database):
    # db.attach("status", status_db)

    prerun_import_oldsheet(db, status_db)
    prerun_update_indexed_column(db, status_db)

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

    with open("./orchard.jsonl", "w") as f:
        for row in combined:
            processed = make_json_from_row(row)
            s = json.dumps(processed)
            f.write(s + "\n")


if __name__ == "__main__":
    file = sys.argv[1]
    status_file = sys.argv[2]
    package(Database(file), Database(status_file))
