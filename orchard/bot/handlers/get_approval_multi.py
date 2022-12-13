from playhouse.shortcuts import model_to_dict

from orchard.bot.lib.constants import DEFAULT_DB_STATUS_VALUE
from orchard.bot.lib.auth import keys
from orchard.bot.lib.entities.status import get_status
from orchard.bot.lib.utils import OrchardJSONResponse
from orchard.db.models import Status

@keys.with_passcode
async def get_approval_multi(request):
    body = await request.json()
    result = [model_to_dict(get_status(id)) for id in body]
    return OrchardJSONResponse(result)