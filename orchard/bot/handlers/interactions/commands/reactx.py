from orchard.bot.lib.comm.message_builder import MessageBuilder
from orchard.bot.lib.slash_commands.slash_router import (
    ApplicationCommandType,
    SlashRoute,
    RouteType,
)
from orchard.bot.lib.comm.interactor import Interactor


async def _reactx(body, _):
    async with Interactor(body["token"]) as i:
        channel_id = body["channel_id"]
        token = body["token"]
        user_id = body["member"]["user"]["id"]
        messages = body["data"]["resolved"]["messages"]
        number_reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for key, value in messages.items():
            message_id = value["id"]
            for reaction in number_reactions:
                if reaction not in [react["emoji"]["name"] for react in value["reactions"]]:
                    continue
                reaction_users = await i.get_reactions(channel_id, message_id, reaction)
                if user_id in [reactor["id"] for reactor in reaction_users.json()]:
                    await i.react(channel_id, message_id, reaction)
            await i.react(channel_id, message_id, "🚫")
        await i.edit(MessageBuilder().content("done."), "@original")


reactx = SlashRoute(
    name="Ignore rdzip attachments",
    description="",
    handler=_reactx,
    default_permission=False,
    defer=RouteType.DEFER_EPHEMERAL,
    type=ApplicationCommandType.MESSAGE,
)
