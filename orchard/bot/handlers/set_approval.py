from playhouse.shortcuts import model_to_dict
from starlette.responses import JSONResponse

from orchard.bot.lib.db import set_status
from orchard.bot.lib import keys
from orchard.bot.lib.typesense import ts_get_by_id
from orchard.db.models import Status


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

    try:
        # the level needs to exist.
        # this throws if the level doesn't exist.
        await ts_get_by_id(id)
        # the level exists if we're here.
        if request.method.lower() == "post":
            body = await request.json()
            set_status(id, body)

        # then get it back.
        return JSONResponse(model_to_dict(Status.get_by_id(id)))

    except Exception as e:
        return JSONResponse({"error": str(e)}, 500)
