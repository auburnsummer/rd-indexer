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


async def update_slash_commands(commands):
    """
    update slash commands
    """
    async with Client() as client:
        r = await client.put(f"{base_url}", json=commands, headers=bot_auth)
    return r
