import asyncio
import pytest
from orchard.bot.lib.comm.crosscode import future, clean, _registry, resolve, wait
from unittest.mock import MagicMock


@pytest.mark.asyncio
async def test_future():
    uuid = future()
    assert uuid is not None
    assert uuid in _registry


@pytest.mark.asyncio
async def test_clean():
    uuid = future()
    clean(uuid)
    assert uuid not in _registry


@pytest.mark.asyncio
async def test_wait_and_resolve():
    mock_func = MagicMock()

    async def wait_on_this(uuid):
        await wait(uuid)
        mock_func()

    # create a uuid
    uuid = future()
    # create a task that waits for it to be set.
    waiter_task = asyncio.create_task(wait_on_this(uuid))
    # sleep for a bit...
    await asyncio.sleep(0)
    # resolve it. wait_on_this coroutine now calls the function.
    resolve(uuid)
    await waiter_task

    mock_func.assert_called_once()
