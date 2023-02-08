from unittest.mock import patch
from orchard.bot.lib.entities.status import StatusHelper
from orchard.db.models import Status
from datetime import datetime, timedelta

import pytest


@pytest.mark.asyncio
async def test_status_create_with_existing(empty_db_with_status_bind, patch_get_level):
    Status.create(id="test_id", approval=5)
    sh = await StatusHelper.create(id="test_id")
    assert sh.to_dict() == {
        "id": "test_id",
        "approval": 5,
        "approval_reasons": None,
        "indexed": None,
    }


@pytest.mark.asyncio
async def test_status_create_with_non_existing_id_creates_default(
    empty_db_with_status_bind, patch_get_level
):
    sh = await StatusHelper.create("does_not_exist")
    assert sh.to_dict() == {
        "id": "does_not_exist",
        "approval": 0,
        "approval_reasons": None,
        "indexed": None,
    }


@pytest.mark.asyncio
async def test_status_set_approval_sets_the_approval(
    empty_db_with_status_bind, patch_get_level
):
    sh = await StatusHelper.create("test_id")
    sh.set_approval(99)
    assert sh.get().approval == 99


@pytest.mark.asyncio
async def test_status_set_approval_updates_indexed_if_newly_approved(
    empty_db_with_status_bind, patch_get_level
):
    sh = await StatusHelper.create("test_id")
    # indexed is originally not set.
    assert sh.get().indexed is None
    _now = datetime.now()
    with patch(
        "orchard.bot.lib.entities.status.datetime.now", wraps=lambda: _now
    ) as mock_datetime:
        sh.set_approval(10)
        assert sh.get().indexed == _now


@pytest.mark.asyncio
async def test_status_set_approval_does_not_update_indexed_if_not_approved(
    empty_db_with_status_bind, patch_get_level
):
    sh = await StatusHelper.create("test_id")
    sh.set_approval(-1)
    assert sh.get().indexed is None


@pytest.mark.asyncio
async def test_status_does_not_update_indexed_if_already_set(
    empty_db_with_status_bind, patch_get_level
):
    time = datetime.now() - timedelta(days=2)
    Status.create(id="test_id", approval=5, indexed=time)
    sh = await StatusHelper.create("test_id")
    sh.set_approval(10)
    assert sh.get().indexed == time
