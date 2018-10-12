import os
import json
import copy

from .ignore import Ignore
from .config import Config
from .errors import TypesNotEqual, \
    ValuesNotEqual, KeyNotExist, LengthsNotEqual, ValueNotFound


NO_DIFF = {}


class Compare:
    config = {}
    rules = {}

    def __init__(self, config=None, rules=None):
        self.set_config(config)
        self.set_ignore_rules(rules)

    def set_config(self, config=None):
        if config is None:
            config = self.get_default_config()
        self.config = Config(config)

    @classmethod
    def get_default_config(cls):
        path = os.path.dirname(__file__) + '/data/config.json'
        with open(path, 'r') as fp:
            return json.load(fp)

    def set_ignore_rules(self, rules=None):
        if rules is None:
            rules = {}
        self.rules = rules

    def check(self, expected, actual):
        e = self.prepare(expected)
        a = self.prepare(actual)
        diff = self._diff(e, a)
        self.report(diff)
        return diff

    def _diff(self, e, a):
        t = type(e)
        if not isinstance(a, t):
            return TypesNotEqual(e, a).explain()
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
        return NO_DIFF

    @classmethod
    def _int_diff(cls, e, a):
        if a == e:
            return NO_DIFF
        return ValuesNotEqual(e, a).explain()

    @classmethod
    def _bool_diff(cls, e, a):
        if a is e:
            return NO_DIFF
        return ValuesNotEqual(e, a).explain()

    @classmethod
    def _str_diff(cls, e, a):
        if a == e:
            return NO_DIFF
        return ValuesNotEqual(e, a).explain()

    def _float_diff(self, e, a):
        if a == e:
            return NO_DIFF
        if self._can_rounded_float():
            p = self._float_precision()
            e, a = round(e, p), round(a, p)
            if a == e:
                return NO_DIFF
        return ValuesNotEqual(e, a).explain()

    def _can_rounded_float(self):
        p = self._float_precision()
        return type(p) is int

    def _float_precision(self):
        path = 'types.float.allow_round'
        return self.config.get(path)

    def _dict_diff(self, e, a):
        d = {}
        for k in e:
            if k not in a:
                d[k] = KeyNotExist(k, None).explain()
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
        path = 'types.list.check_length'
        return self.config.get(path) is True

    def _list_content_diff(self, e, a):
        d = {}
        for i, v in enumerate(e):
            if v in a:
                continue
            t = type(v)
            if t in (int, str, bool, float):
                d[i] = ValueNotFound(v, None).explain()
            elif t is dict:
                d[i] = self._max_diff(v, a, self._dict_diff)
            elif t is list:
                d[i] = self._max_diff(v, a, self._list_diff)
        return self._without_empties(d)

    @classmethod
    def _max_diff(cls, e, l, method):
        t = type(e)
        d = method(e, t())
        for i, v in enumerate(l):
            if type(v) is t:
                dd = method(e, v)
                if len(dd) <= len(d):
                    d = dd
        return d

    @classmethod
    def _list_len_diff(cls, e, a):
        e, a = len(e), len(a)
        if e == a:
            return NO_DIFF
        return LengthsNotEqual(e, a).explain()

    @classmethod
    def _without_empties(cls, d):
        return {k: d[k] for k in d if d[k] != NO_DIFF}

    def report(self, diff):
        if self._need_write_to_console():
            self._write_to_console(diff)
        if self._need_write_to_file():
            self._write_to_file(diff)

    @classmethod
    def _write_to_console(cls, d):
        msg = json.dumps(d, indent=4)
        print(msg)

    def _write_to_file(self, d):
        config = self.config.get('output.file')
        with open(config.pop('name'), 'w') as fp:
            json.dump(d, fp, **config)

    def _need_write_to_console(self):
        path = 'output.console'
        return self.config.get(path) is True

    def _need_write_to_file(self):
        path = 'output.file.name'
        file_name = self.config.get(path)
        return type(file_name) is str

    def prepare(self, x):
        x = copy.deepcopy(x)
        return Ignore.transform(x, self.rules)
