import httpx

from orchard.db.models import Level

def fill_in_params(sql, params):
    text = sql
    # dict of types to a function that makes it suitable for SQL
    sql_encode_funcs = {
        str: lambda s: f'"{s}"',
        bool: lambda b: str(b * 1),
        int: str,
        float: str,
    }
    for param in params:
        # get the appropriate function for the type and call it on the value
        replace = sql_encode_funcs[type(param)](param)
        text = text.replace('?', replace, 1)
    return text

async def _datasette_request(s):
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.rhythm.cafe/datasette/orchard.json", params={"sql": s})
        rj = r.json()
        # convert into Level objects
        levels = [
            Level(**{col: value for col, value in zip(rj['columns'], row)}) for row in rj['rows']
        ]
        return levels

async def datasette_request(query):
    raw_sql = fill_in_params(*query.sql())
    result = await _datasette_request(raw_sql)
    return result