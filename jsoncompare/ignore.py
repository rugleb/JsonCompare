class Ignore:
    rules = None

    def __init__(self, rules):
        self.rules = rules

    def transform(self, o):
        t = type(self.rules)
        if t is dict:
            return self._apply_dict_rules(o, self.rules)
        if t is list:
            return self._apply_list_rules(o, self.rules)
        return o

    def _apply_dict_rules(self, o, rules):
        for k in rules:
            if k not in o:
                continue
            r = rules[k]
            t = type(r)
            if t is list:
                o[k] = self._apply_list_rules(o[k], r)
            elif t is dict:
                o[k] = self._apply_dict_rules(o[k], r)
            elif t is str:
                self._apply_str_rule(o, k, r)
        return o

    @classmethod
    def _apply_list_rules(cls, o, rules):
        return {k: o[k] for k in o if k not in rules}

    @classmethod
    def _apply_str_rule(cls, obj, key, rule):
        if rule == '*':
            del obj[key]
