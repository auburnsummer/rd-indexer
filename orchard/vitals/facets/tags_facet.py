from orchard.vitals.arguments_decorator import with_arguments


@with_arguments("obj")
def tags_facet(obj):
    tags_raw = obj["settings"]["tags"]
    return [s.strip() for s in tags_raw.split(",") if s.strip()]
