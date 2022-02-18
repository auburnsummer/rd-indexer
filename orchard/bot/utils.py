import sqlite3
from orchard.bot.constants import DB_PATH

def get_slash_args(args, body):
    """
    Given a list of args as strings and a body which is a Discord interaction,
    return a list of values corresponding to the given args.
    """
    try:
        options = body["data"]["options"]
        options_dict = {option["name"]: option["value"] for option in options}
        return [options_dict[arg] if arg in options_dict else None for arg in args]
    except KeyError: # No arguments were given (e.g. all arguments are optional and we didn't get any of them)
        return [None for _ in args]


def get_id_from_response(res):
    return res.json()['id']

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# from stackoverflow
class hub_conn():
    def __init__(self):
        self.file=DB_PATH

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = dict_factory
        return self.conn.cursor()
        
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()