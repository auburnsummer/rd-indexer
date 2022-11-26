import pytest
from orchard.db.models import Level

@pytest.fixture
def empty_db_with_level(empty_db):
    Level.bind(empty_db)
    empty_db.create_tables([Level])
    return empty_db