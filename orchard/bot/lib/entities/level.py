from orchard.db.models import Level

def typesense_resp_to_level(json):
    return Level(**json)