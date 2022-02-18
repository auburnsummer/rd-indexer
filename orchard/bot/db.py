from orchard.bot.utils import hub_conn
from orchard.bot.constants import ORCHARD_API_URL
import httpx

from pypika import Query, Table, Field, Parameter


async def datasette_query(sql, shape='array'):
    params = {
        '_shape': shape,
        'sql': sql
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(ORCHARD_API_URL, params=params)
        return resp.json()

def rows_descriptor(column_list):
    return "(" + ",".join(column_list) + ")"

def qmark_descriptor(column_list):
    return "(" + ",".join("?" for _ in column_list) + ")"


async def sync(id):
    """
    Sync a level id from the API to our local copy.
    The local copy doesn't contain a level until its asked for.
    if the level doesn't exist, this command will do nothing, but it won't throw an exception either
    """
    # does it already exist in our copy?
    with hub_conn() as conn:
        curr = conn.execute("SELECT * FROM status WHERE id = ?", [id])
        row = curr.fetchone()
        if row is not None:
            return
    
    # does it exist on the server?
    # datasette is read-only, so we're allowed to do this...
    status_resp = await datasette_query(f"SELECT * FROM status WHERE id = '{id}'", shape="arrays")
    if len(status_resp["rows"]) == 0: # nope, doesn't exist.
        return

    # if we got here then it does exist but we don't have it.
    levels_resp = await datasette_query(f"SELECT * FROM level WHERE id = '{id}'", shape="arrays")
    if len(levels_resp["rows"]) == 0:
        return # shouldn't happen, but check anyway
    
    with hub_conn() as conn:
        # we can build this with string operations because the row names come from datasette which is trusted.
        columns = levels_resp['columns']
        sql = f"INSERT OR IGNORE INTO level {rows_descriptor(columns)} VALUES {qmark_descriptor(columns)}"
        curr = conn.executemany(sql, levels_resp['rows'])
        # ...then insert the status table!
        columns = status_resp['columns']
        sql = f"INSERT OR IGNORE INTO status {rows_descriptor(columns)} VALUES {qmark_descriptor(columns)}"
        curr = conn.executemany(sql, status_resp['rows'])



# schema: https://github.com/auburnsummer/rd-indexer/blob/main/sql/levels.sql
async def get_status(id):
    await sync(id)
    with hub_conn() as conn:
        curr = conn.execute("SELECT * FROM status WHERE id = ?", [id])
        row = curr.fetchone()
        return row

async def set_status(id, obj):
    await sync(id)
    
    table = Table("status")

    q = Query.update(table)
    for pair in obj.items():
        q = q.set(*pair)
    q = q.where(table.id == Parameter(':id'))
    
    with hub_conn() as conn:
        conn.execute(str(q), {'id': id})