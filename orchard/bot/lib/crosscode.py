import asyncio
from orchard.bot.lib.constants import ResponseType
from uuid import uuid4
import textwrap

from starlette.responses import JSONResponse

# Mapping of UUIDs to futures.
_registry = {}


async def future():
    """
    Generate a UUID, add it to the future registry and return it.
    """
    loop = asyncio.get_running_loop()
    new_uuid = uuid4().hex
    new_future = loop.create_future()
    _registry[new_uuid] = new_future
    return new_uuid


def clean(uuid):
    """
    Remove a UUID from the registry.
    """
    if uuid in _registry:
        del _registry[uuid]


async def refresh(uuid):
    """
    Refresh a future in the registry so it can be used again.
    """
    loop = asyncio.get_running_loop()
    new_future = loop.create_future()
    _registry[uuid] = new_future


async def handle(body):
    uuid = body["data"]["custom_id"]
    if uuid in _registry and not _registry[uuid].done():
        _registry[uuid].set_result(uuid)
        await refresh(uuid)
        return JSONResponse({"type": ResponseType.DEFERRED_UPDATE_MESSAGE})
    else:
        error_text = textwrap.dedent(
            f"""
            The crosscode UUID {uuid} either doesn't exist or has been used without a refresh.
            This may be because I've restarted the server in the middle of an interaction. Please try
            the slash command again.

            If this error continues, ping auburn. 
        """
        )
        return JSONResponse(
            {"type": ResponseType.UPDATE_MESSAGE, "data": {"content": error_text}}
        )


async def button_press(*uuids):
    futures = [_registry[uuid] for uuid in uuids]
    done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
    return list(done)[0].result() if len(done) else False
