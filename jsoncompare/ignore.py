from abc import ABC


class Ignore(ABC):

    @classmethod
    def transform(cls, obj, rules):
        t = type(rules)
        if t is dict:
            return cls._apply_dictable_rule(obj, rules)
        if t is list:
            return cls._apply_listable_rule(obj, rules)
        return obj

    @classmethod
    def _apply_dictable_rule(cls, obj, rules):
        for key in rules:
            rule = rules[key]
            if cls._is_special_key(key):
                obj = cls._apply_special_rule(key, obj, rule)
            elif type(rule) is str:
                obj = cls._apply_stringable_rule(key, obj, rule)
            elif key in obj:
                obj[key] = cls.transform(obj[key], rule)
        return obj

    @classmethod
    def _apply_listable_rule(cls, obj, rules):
        for i in rules:
            if i in obj:
                del obj[i]
        return obj

    @classmethod
    def _apply_stringable_rule(cls, key, obj, rule):
        if rule == '*':
            if key in obj:
                del obj[key]
        return obj

    @classmethod
    def _is_special_key(cls, key):
        return key.startswith('_')

    @classmethod
    def _apply_special_rule(cls, key, obj, rule):
        if key == '_values':
            return cls._ignore_values(obj, rule)
        if key == '_list':
            return cls._ignore_list_items(obj, rule)
        return obj

    @classmethod
    def _ignore_list_items(cls, obj, rule):
        return [cls.transform(x, rule) for x in obj]

    @classmethod
    def _ignore_values(cls, obj, black_list):
        t = type(obj)
        if t is list:
            return [x for x in obj if x not in black_list]
        if t is obj:
            return {k: obj[k] for k in obj if k not in black_list}
        return obj
