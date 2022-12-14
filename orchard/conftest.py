import pytest
import debugpy
from playhouse.sqlite_ext import SqliteExtDatabase
import tempfile

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