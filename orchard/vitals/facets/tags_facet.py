def tags_facet(obj, _):
    tags_raw = obj["settings"]["tags"]
    return [s.strip() for s in tags_raw.split(",") if s.strip()]
