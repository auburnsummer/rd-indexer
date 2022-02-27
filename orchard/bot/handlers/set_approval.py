from starlette.applications import Starlette
from starlette.responses import JSONResponse

from orchard.bot.db import get_status, set_status
from orchard.bot import keys


async def set_approval(request):
    # authorization...
    try:
        if "authorization" not in request.headers:
            raise ValueError("There should be an Authorization header, but there aint")
        token_type, token = request.headers["authorization"].split(" ")
        if token_type.lower() != "bearer":
            raise ValueError("Token type should be Bearer.")
        keys.check_passcode(token)

    except Exception as e:
        return JSONResponse({"error": str(e)}, 401)

    # return JSONResponse({'hello': 'world'}, 200);

    # get stuff out from the body?
    id = request.path_params["id"]

    try:
        if request.method.lower() == "post":
            body = await request.json()
            await set_status(id, body)
            return JSONResponse(await get_status(id))
        else:
            # it's a get request.
            return JSONResponse(await get_status(id))
    except Exception as e:
        return JSONResponse({"error": str(e)}, 500)
