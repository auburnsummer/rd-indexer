import httpx
import pytest
import debugpy
from playhouse.sqlite_ext import SqliteExtDatabase
import tempfile

from unittest.mock import patch

@pytest.fixture
def empty_db():
    # Use an actual file, as sqlite will terminate in-memory databases early if the connection is closed.
    with tempfile.NamedTemporaryFile() as f:
        db = SqliteExtDatabase(f.name)
        yield db
        db.close()

@pytest.fixture
def debug():
    debugpy.listen(5678)
    debugpy.wait_for_client()  # blocks execution until client is attached


@pytest.fixture(autouse=True)
def block_httpx(httpx_mock):
    yield

@pytest.fixture
def assert_all_responses_were_requested(autouse=True) -> bool:
    return False