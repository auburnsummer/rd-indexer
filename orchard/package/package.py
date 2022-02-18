from datetime import datetime
import json
import sys
from math import floor

from sqlite_utils import Database
import itertools
from orchard.scan.schema import LEVEL_SCHEMA

def make_json_from_row(row):
    type_transformers = {
        bool : lambda n : True if n > 0 else False,
        datetime : lambda s : floor(datetime.fromisoformat(s).timestamp()),
    }
    key_transformers = {
        "tags": lambda s: json.loads(s),
        "authors": lambda s: json.loads(s),
    }
    for col_name, col_value in row.items():
        col_type = LEVEL_SCHEMA[col_name]
        if col_type in type_transformers.keys():
            row[col_name] = type_transformers[col_type](col_value)
        if col_name in key_transformers.keys():
            row[col_name] = key_transformers[col_name](col_value)

    return row


def package(db: Database):
    with open("./orchard.jsonl", "w") as f:
        for row in db["level"].rows:
            processed = make_json_from_row(row)
            s = json.dumps(processed)
            f.write(s + "\n")

if __name__ == "__main__":
    file = sys.argv[1]
    package(Database(file))