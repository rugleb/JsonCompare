import re
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
            elif cls._is_regex_rule(rule):
                obj = cls._apply_regex_rule(key, obj, rule)
            elif type(rule) is str:
                obj = cls._apply_stringable_rule(key, obj, rule)
            elif key in obj:
                obj[key] = cls.transform(obj[key], rule)
        return obj

    @classmethod
    def _apply_listable_rule(cls, obj, rules):
        for key in rules:
            if type(key) is dict:
                for index, y in enumerate(obj):
                    obj[index] = cls.transform(obj[index], key)
            elif key in obj:
                del obj[key]
        return obj

    @classmethod
    def _apply_stringable_rule(cls, key, obj, rule):
        if rule == '*':
            if key in obj:
                del obj[key]
        return obj

    @classmethod
    def _is_regex_rule(cls, rule):
        return type(rule) is dict and '_re' in rule

    @classmethod
    def _apply_regex_rule(cls, key, obj, rule):
        regex = rule['_re']
        if key in obj and re.match(regex, obj[key]):
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
        if key == '_range':
            return cls._ignore_range(obj, rule)
        return obj

    @classmethod
    def _ignore_list_items(cls, obj, rule):
        return [cls.transform(x, rule) for x in obj]

    @classmethod
    def _ignore_values(cls, obj, black_list):
        t = type(obj)
        if t is list:
            return [x for x in obj if x not in black_list]
        if t is dict:
            return {k: obj[k] for k in obj if k not in black_list}
        return obj

    @classmethod
    def _ignore_range(cls, obj, rule):
        t = type(obj)
        if t is int or t is float:
            return rule[0] <= obj and obj <= rule[1]
        return obj
