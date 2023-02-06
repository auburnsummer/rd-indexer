import pytest
from orchard.bot.lib.entities.status import StatusHelper
from orchard.bot.lib.entities.user import UserHelper


def test_user_create(empty_db_with_status_bind):
    uh = UserHelper.create("test_user")
    assert uh.to_dict() == {"id": "test_user", "selected_level": None}


@pytest.mark.asyncio
async def test_user_set_level(empty_db_with_status_bind, patch_get_level):
    uh = UserHelper.create("test_user")
    sh = await StatusHelper.create("test_id")
    uh.set_selected_level(sh.get())
    assert uh.to_dict() == {"id": "test_user", "selected_level": sh.to_dict()}
