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


def is_equal_types(first, second):
    return type(first) is type(second)


def is_not_equal_types(first, second):
    return not is_equal_types(first, second)


def is_primitive(o):
    return type(o) in (int, bool, str)


def is_not_primitive(o):
    return not is_primitive(o)


def is_iterable(o):
    return type(o) in (dict, list, tuple, set)


def is_not_iterable(o):
    return not is_iterable(o)
