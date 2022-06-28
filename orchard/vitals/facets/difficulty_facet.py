from orchard.vitals.arguments_decorator import with_arguments

DIFFICULTIES = ["Easy", "Medium", "Tough", "VeryTough"]


@with_arguments("obj")
def difficulty_facet(obj):
    try:
        diff_string = obj["settings"]["difficulty"]
        return DIFFICULTIES.index(diff_string)
    except (ValueError, KeyError):
        return 1  # medium
