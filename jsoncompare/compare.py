import os
import json
import copy

from jsoncompare.errors import TypesNotEqual, ValuesNotEqual, KeyNotExist, LengthNotEqual, ValueNotFound


class Compare:
    config = {}

    def __init__(self, config=None):
        self.set_config(config)

    def set_config(self, config=None):
        if config is None:
            config = self.get_default_config()
        self.config = config

    @classmethod
    def get_default_config(cls):
        path = os.path.dirname(__file__) + '/data/config.json'
        with open(path, 'r') as fp:
            return json.load(fp)

    def check(self, expected, actual):
        e = self.prepare(expected)
        a = self.prepare(actual)
        return self._diff(e, a) == {}

    def _diff(self, e, a):
        t = type(e)
        if not isinstance(a, t):
            return TypesNotEqual(e, a)
        if t is int:
            return self._int_diff(e, a)
        if t is str:
            return self._str_diff(e, a)
        if t is bool:
            return self._bool_diff(e, a)
        if t is float:
            return self._float_diff(e, a)
        if t is dict:
            return self._dict_diff(e, a)
        if t is list:
            return self._list_diff(e, a)
        return {}

    @classmethod
    def _int_diff(cls, e, a):
        if a == e:
            return {}
        return ValuesNotEqual(e, a)

    @classmethod
    def _bool_diff(cls, e, a):
        if a is e:
            return {}
        return ValuesNotEqual(e, a)

    @classmethod
    def _str_diff(cls, e, a):
        if a == e:
            return {}
        return ValuesNotEqual(e, a)

    def _float_diff(self, e, a):
        if a == e:
            return {}
        if self._can_rounded_float():
            e = round(e, 2)
            a = round(a, 2)
            if a == e:
                return {}
        return ValuesNotEqual(e, a)

    def _can_rounded_float(self):
        return True

    def _dict_diff(self, e, a):
        d = {}
        for k in e:
            if k not in a:
                d[k] = KeyNotExist(k, None)
            else:
                d[k] = self._diff(e[k], a[k])
        return self._without_empties(d)

    def _list_diff(self, e, a):
        d = {}
        if self._need_compare_length():
            d['_length'] = self._list_len_diff(e, a)
        d['_content'] = self._list_content_diff(e, a)
        return self._without_empties(d)

    def _need_compare_length(self):
        return True

    def _list_content_diff(self, e, a):
        d = {}
        for i, v in enumerate(e):
            if v in a:
                continue
            t = type(v)
            if t in (int, str, bool, float):
                d[i] = ValueNotFound(v, None)
            elif t is dict:
                d[i] = self._dict_diff(v, {})
                for ii, vv in enumerate(a):
                    if type(vv) is dict:
                        dd = self._dict_diff(v, vv)
                        if len(dd) <= len(d[i]):
                            d[i] = dd
            elif t is list:
                d[i] = self._list_diff(v, [])
                for ii, vv in enumerate(a):
                    if type(vv) is list:
                        dd = self._list_diff(v, vv)
                        if len(dd) <= len(d[i]):
                            d[i] = dd
        return self._without_empties(d)

    @classmethod
    def _list_len_diff(cls, e, a):
        e_len = len(e)
        a_len = len(a)
        if a_len == e_len:
            return {}
        return LengthNotEqual(e_len, a_len)

    @classmethod
    def _without_empties(cls, d):
        return {k: d[k] for k in d if d[k] != {}}

    def report(self, diff):
        pass

    @classmethod
    def prepare(cls, x):
        return copy.deepcopy(x)
