from starlette.responses import JSONResponse

from orchard.bot import keys
from orchard.bot.db import get_or_default


async def get_approval_multi(request):
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
    body = await request.json()
    db = request.app.state.db

    result = [get_or_default(db, id, 0) for id in body]
    return JSONResponse(result)