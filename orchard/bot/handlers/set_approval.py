from starlette.applications import Starlette
from starlette.responses import JSONResponse

from orchard.bot.db import get_or_default, set_status
from orchard.bot import keys
from orchard.bot.typesense import get_by_id


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

    # get stuff out from the body?
    id = request.path_params["id"]
    db = request.app.state.db


    try:
        # the level needs to exist
        await get_by_id(id)
        if request.method.lower() == "post":
            body = await request.json()
            set_status(db, id, body)
            return JSONResponse(get_or_default(db, id, 0))
        else:
            # it's a get request.
            return JSONResponse(get_or_default(db, id, 0))
    except Exception as e:
        return JSONResponse({"error": str(e)}, 500)
