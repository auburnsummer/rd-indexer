from orchard.bot.lib.entities.status import StatusHelper
from orchard.bot.lib.auth import keys
from orchard.bot.lib.utils import OrchardJSONResponse

import logging

logger = logging.getLogger(__name__)


@keys.with_passcode
async def set_approval(request):
    """
    Get or set an approval value for a level.
    """
    id = request.path_params["id"]

    sh = await StatusHelper.create(id)

    if request.method.lower() == "post":
        body = await request.json()
        approval = body["approval"]
        sh.set_approval(approval)

    return OrchardJSONResponse(sh.to_dict())
