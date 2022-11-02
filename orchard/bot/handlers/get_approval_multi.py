from playhouse.shortcuts import model_to_dict
from starlette.responses import JSONResponse

from orchard.bot.constants import DEFAULT_DB_STATUS_VALUE
from orchard.bot.lib import keys
from orchard.bot.lib.utils import OrchardJSONResponse
from orchard.db.models import Status


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
        return OrchardJSONResponse({"error": str(e)}, 401)

    body = await request.json()

    result = [
        model_to_dict(Status.get_or_create(
            id=id,
            defaults=DEFAULT_DB_STATUS_VALUE
        )[0]) for id in body
    ]

    return OrchardJSONResponse(result)