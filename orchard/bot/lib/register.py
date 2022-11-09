from orchard.utils.client import Client
from orchard.bot.lib.constants import BOT_TOKEN, APPLICATION_ID, DEV_GUILD
from orchard.utils.constants import DISCORD_API_URL

bot_auth = {"Authorization": f"Bot {BOT_TOKEN}"}

# DEV_GUILD is False if env variable not defined
if DEV_GUILD:
    base_url = (
        f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/guilds/{DEV_GUILD}/commands"
    )
else:
    base_url = f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/commands"

"""
Get a list of all current slash commands.
"""


async def current_slash_commands():
    async with Client() as client:
        r = await client.get(base_url, headers=bot_auth)
    return r.json()


"""
Remove a global slash command.
"""


async def remove_slash_command(id):
    async with Client() as client:
        r = await client.delete(f"{base_url}/{id}", headers=bot_auth)
    return r


"""
update slash commands
"""


async def update_slash_commands(commands):
    async with Client() as client:
        r = await client.put(f"{base_url}", json=commands, headers=bot_auth)
    return r


"""
wefawefawef
"""


def get_command_to_id_mapping(json_resp):
    return {c["name"]: c["id"] for c in json_resp}


"""
update permissions
"""


async def update_slash_permissions(permissions):
    if DEV_GUILD:
        async with Client() as client:
            r = await client.put(
                f"{base_url}/permissions", json=permissions, headers=bot_auth
            )
        return r
