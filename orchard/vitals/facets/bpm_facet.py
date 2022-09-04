from orchard.utils.dig import try_dig
from orchard.vitals.arguments_decorator import with_arguments


def is_bpm_event(evt):
    return evt["type"] in ["PlaySong", "SetBeatsPerMinute"]


def get_bpm_from_event(evt):
    # then, the bpm is either in the ["bpm"] or ["beatsPerMinute"] key
    try:
        return evt["bpm"]
    except KeyError:
        return evt["beatsPerMinute"]

@with_arguments("obj", "toml")
def bpm_facet(obj, toml):
    # is it declared in the TOML?
    if toml is not None and try_dig(["bpm", "max"], toml) and try_dig(["bpm", "min"], toml):
        return try_dig(["bpm", "max"], toml), try_dig(["bpm", "min"], toml)

    bpms = [get_bpm_from_event(e) for e in obj["events"] if is_bpm_event(e)]
    # then, the bpm is either in the ["bpm"] or ["beatsPerMinute"] key
    if len(bpms) == 0:
        return 0, 0
    return max(bpms), min(bpms)
