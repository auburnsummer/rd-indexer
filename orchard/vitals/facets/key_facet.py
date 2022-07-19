import logging

from orchard.parse.utils import dig
from orchard.vitals.arguments_decorator import with_arguments

logger = logging.getLogger(__name__)


def make_key_facet(path, fallback=None):
    @with_arguments("obj")
    def inner(obj):
        try:
            return dig(path, obj)
        except KeyError:
            logger.info(f"Key {path} not found, going to fallback.")
            return fallback

    return inner
