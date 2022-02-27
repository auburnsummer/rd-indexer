from orchard.bot.constants import ResponseType
from starlette.responses import JSONResponse


def ping(body, _):
    # Using the JSONResponse constructor, return a response as follows:
    #  - the return code should be 200
    #  - the response body should be a JSON object with a key 'type' whose value is 4
    #  - the response body should have a key 'data.content' whose value is 'pong'
    return JSONResponse(
        {"type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE, "data": {"content": "pong"}}
    )
