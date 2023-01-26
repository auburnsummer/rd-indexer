
from orchard.bot.lib.ext.datasette import datasette_request
from orchard.db.models import Level

class LevelDoesNotExist(Exception): pass
from aiocache import Cache, cached

@cached(cache=Cache.MEMORY)
async def get_level(id: str):
    """
    Get a level if it exists. Otherwise, throw an exception.
    """
    resp = await datasette_request(Level.select().where(Level.id == id))
    if resp:
        return resp[0]
    else:
        raise LevelDoesNotExist(f"I could not find a level id with {id}.")

