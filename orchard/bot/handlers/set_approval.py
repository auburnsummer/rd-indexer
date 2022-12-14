from playhouse.shortcuts import model_to_dict
from starlette.responses import JSONResponse

from orchard.bot.lib.entities.status import get_status, set_status
from orchard.bot.lib.auth import keys
from orchard.bot.lib.ext.datasette import datasette_request
from orchard.bot.lib.utils import OrchardJSONResponse
from orchard.db.models import Level, Status

import logging

logger = logging.getLogger(__name__)

@keys.with_passcode
async def set_approval(request):
    # get stuff out from the body?
    id = request.path_params["id"]

    # try to get the level.
    level = await datasette_request(Level.select().where(Level.id == id))
    if level:
        if request.method.lower() == "post":
            body = await request.json()
            set_status(id, body)
        final = model_to_dict(get_status(id))
        return OrchardJSONResponse(final)
    else:
        return OrchardJSONResponse({"error": f"The level {id} does not exist."}, 500)
