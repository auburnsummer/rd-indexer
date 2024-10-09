from orchard.bot.lib.comm.message_builder import MessageBuilder
from orchard.bot.lib.slash_commands.slash_router import (
    ApplicationCommandType,
    SlashRoute,
    RouteType,
)
from orchard.bot.lib.comm.interactor import Interactor


async def _reactx(body, _):
    async with Interactor(body["token"]) as interactor:
        channel_id = body["channel_id"]
        user_id = body["member"]["user"]["id"]
        bot_id = body["application_id"]
        messages = body["data"]["resolved"]["messages"]
        number_reactions = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
        ]
        ignored_rdzips = []
        for key, value in messages.items():
            message_id = value["id"]
            rdzip_attachments = [
                attachment["filename"]
                for attachment in value["attachments"]
                if attachment["filename"].endswith(".rdzip")
            ]
            for i, attachment in enumerate(rdzip_attachments):
                if "reactions" not in value:
                    continue
                if number_reactions[i] not in [
                    react["emoji"]["name"] for react in value["reactions"]
                ]:
                    continue
                reactions = await interactor.get_reactions(
                    channel_id, message_id, number_reactions[i]
                )
                reaction_users = [react["id"] for react in reactions.json()]
                if bot_id in reaction_users:
                    ignored_rdzips.append(attachment)
                    continue
                if user_id in reaction_users:
                    ignored_rdzips.append(attachment)
                    interactor.react(channel_id, message_id, number_reactions[i])
            await interactor.react(channel_id, message_id, "🚫")
        result = "Done, now ignoring all rdzips."
        if len(ignored_rdzips) > 0:
            result = (
                "Done, now ignoring the following rdzips:\n```"
                + "\n".join(ignored_rdzips)
                + "\n```"
            )
        await interactor.edit(MessageBuilder().content(result), "@original")


reactx = SlashRoute(
    name="reactx",
    description="",
    handler=_reactx,
    default_permission=False,
    defer=RouteType.DEFER_EPHEMERAL,
    type=ApplicationCommandType.MESSAGE,
)
