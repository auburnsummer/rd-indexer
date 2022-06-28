# get something from a json dictionary, array, etc by a list of properties
def dig(dig_list, obj):
    final = obj
    for prop in dig_list:
        final = final[prop]
    return final

def try_dig(dig_list, obj):
    if obj is None:
        return None
    try:
        return dig(dig_list, obj)
    except KeyError:
        return None


def update(obj, key, value):
    if obj is None:
        return value
    else:
        subpath = dig(key[0:-1], obj)
        if key[-1] == -1:
            subpath.append(value)
        else:
            subpath[key[-1]] = value
        return obj
