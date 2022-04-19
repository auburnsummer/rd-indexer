import logging

from orchard.parse.utils import dig

logger = logging.getLogger(__name__)


def make_key_facet(path, fallback=None):
    def inner(obj, *_):
        try:
            return dig(path, obj)
        except KeyError:
            logger.info(f"Key {path} not found, going to fallback.")
            return fallback

    return inner
