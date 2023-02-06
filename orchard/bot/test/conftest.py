from unittest.mock import patch
import pytest
from orchard.db.models import Status, User


@pytest.fixture
def empty_db_with_status_bind(empty_db):
    with Status.bind_ctx(empty_db):
        empty_db.create_tables([Status])
        with User.bind_ctx(empty_db):
            empty_db.create_tables([User])
            yield empty_db


@pytest.fixture
def patch_get_level():
    async def fake_get_level(_):
        return True

    with patch("orchard.bot.lib.entities.level._get_level", wraps=fake_get_level):
        yield
