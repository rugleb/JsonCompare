def is_dict(o):
    return isinstance(o, dict)


def is_not_dict(o):
    return not is_dict(o)


def is_bool(o):
    return type(o) is bool


def is_not_bool(o):
    return not is_bool(o)


def is_list(o):
    return isinstance(o, list)


def is_not_list(o):
    return not is_list(o)
