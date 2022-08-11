from starlette.responses import FileResponse
import sys

async def status_dot_db(request):
    return FileResponse(sys.argv[1], media_type="application/x-sqlite3")
