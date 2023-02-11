"""
pager is the module that handles the communication between component interactions
(button presses, etc.) and the command functions.

beep beep, beep beep, beep beep, beep
"""

import asyncio
from typing import Dict, NewType
from orchard.bot.lib.constants import ResponseType
from uuid import uuid4
import textwrap

from starlette.responses import JSONResponse

PagerUUID = NewType("PagerUUID", str)

# Mapping of UUIDs to futures.
_registry: Dict[PagerUUID, asyncio.Event] = {}


def new():
    """
    Generate a UUID, add it to the event registry and return it.
    """
    new_uuid = PagerUUID(uuid4().hex)
    evt = asyncio.Event()
    _registry[new_uuid] = evt
    return new_uuid


def clean(uuid: PagerUUID):
    """
    Remove a UUID from the registry.
    """
    if uuid in _registry:
        del _registry[uuid]


async def wait(uuid: PagerUUID):
    """
    Wait on a uuid to finish, then return that uuid.
    """
    if uuid in _registry:
        await _registry[uuid].wait()
    return uuid


def resolve(uuid: PagerUUID):
    if uuid in _registry:
        _registry[uuid].set()
        # if the coroutine is in a loop, etc. it might want the same button again.
        _registry[uuid].clear()


async def handle(body):
    """
    Called if we received a type 3 (component) interaction.
    """
    # discord attaches the UUID of the button to this property.
    uuid = PagerUUID(body["data"]["custom_id"])
    if uuid in _registry and not _registry[uuid].is_set():
        # complete the future. this causes the coroutine to resume.
        resolve(uuid)
        # respond to the button press. we don't ever respond directly, the coroutine should be handling the actual response.
        return JSONResponse({"type": ResponseType.DEFERRED_UPDATE_MESSAGE})
    else:
        error_text = textwrap.dedent(
            f"""
            I recieved a component interaction {uuid}, but I don't know how to deal with it.
            This may be because I've restarted the server in the middle of an interaction. Please try
            the slash command again.

            If this error continues, ping auburn. 
        """
        )
        return JSONResponse(
            {"type": ResponseType.UPDATE_MESSAGE, "data": {"content": error_text}}
        )
