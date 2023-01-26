
# https://stackoverflow.com/a/60758313

from orchard.bot.lib.entities.level import get_level
from orchard.db.models import User

def get_user(id):
    current, _ = User.get_or_create(
        id=id,
        selected_level=None
    )
    return current

async def set_selected_level(id):
    level = await get_level(id)
    # just checking it exists.
    user = get_user()



def get_selected_level(id):
    pass