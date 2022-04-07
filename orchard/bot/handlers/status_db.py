import os

from sqlite_utils import Database
from starlette.responses import FileResponse, JSONResponse, Response
import sys

from orchard.bot.constants import POST_STATUS_DOT_DB_TOKEN


async def post_status_dot_db(request):
    try:
        if "authorization" not in request.headers:
            raise ValueError("There should be an Authorization header, but there aint")
        token_type, token = request.headers["authorization"].split(" ")
        if token_type.lower() != "bearer":
            raise ValueError("Token type should be Bearer.")
        if token != POST_STATUS_DOT_DB_TOKEN:
            raise ValueError("Token incorrect")
    except Exception as e:
        return JSONResponse({"error": str(e)}, 401)

    # delete old db
    db = request.app.state.db
    db.conn.close()
    os.remove(sys.argv[1])
    # add given new db
    with open(sys.argv[1], "wb") as f:
        f.write(await request.body())

    request.app.state.db = Database(sys.argv[1])


async def status_dot_db(request):
    if request.method.lower() == 'post':
        await post_status_dot_db(request)
        return Response(status_code=204)
    else:
        return FileResponse(sys.argv[1], media_type="application/x-sqlite3")
