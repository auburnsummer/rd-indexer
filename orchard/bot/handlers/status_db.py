from starlette.responses import Response
import tempfile

async def status_dot_db(request):
    db = request.app.state.db
    with tempfile.NamedTemporaryFile() as temp:
        db.execute_sql(f"""
VACUUM INTO "{temp.name}"
        """)
        temp.seek(0)
        contents = temp.read()
        return Response(contents, media_type="application/vnd.sqlite3")