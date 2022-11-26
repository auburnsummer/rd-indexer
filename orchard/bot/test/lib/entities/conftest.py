
import json
from pathlib import Path
import pytest

from orchard.db.models import Status

@pytest.fixture
def empty_db_with_status_bind(empty_db):
    Status.bind(empty_db)
    empty_db.create_tables([Status])
    return empty_db

@pytest.fixture
def typesense_fixtures():
    files = Path(__file__).parent.resolve().glob("./fixtures/**/*.json")
    final = []
    for file in files:
        with file.open("r") as f:
            final.append(json.loads(f.read()))
    
    return final

@pytest.fixture
def get_by_id(typesense_fixtures):
    def inner(id):
        for fixture in typesense_fixtures:
            for document in (f["document"] for f in fixture["hits"]):
                if document["id"] == id:
                    return document
        
        print(f"get_by_id could not find id {id}")
        assert False
    return inner

@pytest.fixture
def typesense_client(typesense_fixtures):
    pass