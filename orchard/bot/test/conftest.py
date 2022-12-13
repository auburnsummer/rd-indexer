import pytest
from orchard.db.models import Status

@pytest.fixture
def empty_db_with_status_bind(empty_db):
    with Status.bind_ctx(empty_db):
        empty_db.create_tables([Status])
        yield empty_db