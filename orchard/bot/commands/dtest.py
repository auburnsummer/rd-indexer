from orchard.bot.utils import get_id_from_response
from orchard.bot.interactions import Interactor
from orchard.bot.message_builder import ActionRow, Button, MessageBuilder as M

import orchard.bot.crosscode as cc

async def dtest(body, _):
    async with Interactor(body["token"]) as i:

        await i.edit(M().content("ayayayayayaya"), "@original")

        [b1, b2] = [await i.uuid() for _ in range(2)]

        p2 = get_id_from_response(await i.post(
            M()
            .content("popopopopo")
            .ephemeral()
            .row(
                ActionRow(
                    Button(label="Left", custom_id=b1),
                    Button(label="right", custom_id=b2)
                )
            )
        ))

        clicked = await cc.button_press(b1, b2)

        if clicked == b1:
            text = "you clicked left!"
        elif clicked == b2:
            text = "you clicked right!"
        else:
            text = "errr"

        print("you clicked!")
        print(clicked)
        await i.edit(M().content(text).clear_rows(), p2)


        # await i.post({
        #     "content": "popopopopopo",
        #     "components": [
        #         {
        #             "type": 1,
        #             "components": [
        #                 {
        #                     "type": 2,
        #                     "label": "Click me!",
        #                     "style": 1,
        #                     "custom_id": "click_one"
        #                 }
        #             ]
        #         }
        #     ]
        # })
