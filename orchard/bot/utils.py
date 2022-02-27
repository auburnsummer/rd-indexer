import sqlite3
import itertools


def get_slash_args(args, body):
    """
    Given a list of args as strings and a body which is a Discord interaction,
    return a list of values corresponding to the given args.
    """
    try:
        options = body["data"]["options"]
        options_dict = {option["name"]: option["value"] for option in options}
        return [options_dict[arg] if arg in options_dict else None for arg in args]
    except KeyError:  # No arguments were given (e.g. all arguments are optional and we didn't get any of them)
        return [None for _ in args]


def get_id_from_response(res):
    return res.json()["id"]


def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
