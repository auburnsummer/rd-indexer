from orchard.bot.crosscode import button_press
from orchard.bot.utils import get_id_from_response, get_slash_args
from orchard.bot.interactions import Interactor
from orchard.bot.message_builder import ActionRow, Button, MessageBuilder as M

async def counter(body, _):
    [incr] = get_slash_args(['increment'], body)


    async with Interactor(body["token"]) as i:

        # Get the ID of the original "pending" message.
        # We have to do this instead of using @original because we make a new post _before_ editing the original message...
        # and in that scenario, Discord assigns the @original to the new post instead.
        original = get_id_from_response(await i.get("@original"))

        curr_count = 0
        
        [incr_button, finish_button] = [await i.uuid() for _ in range(2)]

        # post the initial buttons.
        button_message = get_id_from_response(await i.post(
            M()
            .content("Press the increment button to increase the number.")
            .ephemeral()
            .row(
                ActionRow(
                    Button(label="increment", custom_id=incr_button),
                    Button(label="done", custom_id=finish_button)
                )
            )
        ))
            
        while True:
            # Edit the message with the current count.
            await i.edit(M().content(f"{curr_count}"), original)

            # Wait for a button to be pressed.
            pressed = await button_press(incr_button, finish_button)

            if pressed == incr_button:
                curr_count += incr
            else:
                break

        # Remove the initial button message.
        # not sure why, but for some messages editing to an empty message works better than deleting.
        await i.edit(M().clear_rows(), button_message)

        

