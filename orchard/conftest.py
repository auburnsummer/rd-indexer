import pytest
from playhouse.sqlite_ext import SqliteExtDatabase

@pytest.fixture
def empty_db():
    db = SqliteExtDatabase(":memory:")
    return db