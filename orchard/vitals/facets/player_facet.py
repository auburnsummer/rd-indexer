from orchard.parse.utils import try_dig
from orchard.vitals.arguments_decorator import with_arguments


@with_arguments("obj", "toml")
def player_facet(obj, toml):
    s = obj["settings"]["canBePlayedOn"]
    toml_1 = try_dig(["modes", "1p"], toml)
    toml_2 = try_dig(["modes", "2p"], toml)
    single_player = toml_1 if toml_1 is not None else s in ["OnePlayerOnly", "BothModes"]
    two_player = toml_2 if toml_2 is not None else s in ["TwoPlayerOnly", "BothModes"]
    return single_player, two_player
