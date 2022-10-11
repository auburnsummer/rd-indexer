import logging

from orchard.utils.dig import dig
from orchard.vitals.arguments_decorator import with_arguments
from orchard.vitals.color_tagged_string import parse_color_tagged_string

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


def make_color_enabled_key_facet(path, fallback=None):
    @with_arguments("obj")
    def inner(obj):
        try:
            content = dig(path, obj)
            stripped, colors = parse_color_tagged_string(content)
            return stripped, colors
        except KeyError:
            logger.info(f"Key {path} not found, going to fallback.")
            return fallback, []

    return inner
