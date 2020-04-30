import json
import copy

from .ignore import Ignore
from .config import Config
from .errors import TypesNotEqual, \
    ValuesNotEqual, KeyNotExist, LengthsNotEqual, ValueNotFound


NO_DIFF = {}
NO_RULES = {}

DEFAULT_CONFIG = {
    'output': {
        'console': False,
        'file': {
            'allow_nan': True,
            'ensure_ascii': True,
            'indent': 4,
            'name': None,
            'skipkeys': True,
        },
    },
    'types': {
        'float': {
            'allow_round': 2,
        },
        'list': {
            'check_length': True,
        }
    }
}


class Compare:
    
    __slots__ = ("_config", "_rules")

    def __init__(self, config: dict = None, rules: dict = None):
        if not config:
            config = DEFAULT_CONFIG
        if not rules:
            rules = NO_RULES

        self._config = Config(config)
        self._rules = rules

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
        return self._config.get(path)

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
        return self._config.get(path) is True

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
        config = self._config.get('output.file')
        with open(config.pop('name'), 'w') as fp:
            json.dump(d, fp, **config)

    def _need_write_to_console(self):
        path = 'output.console'
        return self._config.get(path) is True

    def _need_write_to_file(self):
        path = 'output.file.name'
        file_name = self._config.get(path)
        return type(file_name) is str

    def prepare(self, x):
        x = copy.deepcopy(x)
        return Ignore.transform(x, self._rules)
