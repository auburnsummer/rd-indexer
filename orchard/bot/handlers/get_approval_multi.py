from playhouse.shortcuts import model_to_dict

from orchard.bot.lib.auth import keys
from orchard.bot.lib.entities.status import _get_status
from orchard.bot.lib.utils import OrchardJSONResponse


@keys.with_passcode
async def get_approval_multi(request):
    body = await request.json()
    result = [model_to_dict(_get_status(id)) for id in body]
    return OrchardJSONResponse(result)
