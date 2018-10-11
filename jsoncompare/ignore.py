class Ignore:
    rules = None

    def __init__(self, rules):
        self.rules = rules

    def transform(self, obj):
        t = type(self.rules)
        if t is dict:
            return self._apply_dictable_rules(obj, self.rules)
        if t is list:
            return self._apply_listable_rules(obj, self.rules)
        return obj

    def _apply_dictable_rules(self, obj, rules):
        for key in rules:
            rule = rules[key]
            if key.startswith('_'):
                if key == '_values':
                    obj = self._ignore_values(obj, rule)
                elif key == '_list':
                    pass
            elif type(rule) is str:
                if rule == '*':
                    if key in obj:
                        del obj[key]
            elif type(rule) is list:
                if key in obj:
                    obj[key] = self._apply_listable_rules(obj[key], rule)
            elif type(rule) is dict:
                if key in obj:
                    obj[key] = self._apply_dictable_rules(obj[key], rule)
        return obj

    @classmethod
    def _ignore_values(cls, obj, black_list):
        t = type(obj)
        if t is list:
            return [x for x in obj if x not in black_list]
        if t is obj:
            return {k: obj[k] for k in obj if k not in black_list}
        return obj

    @classmethod
    def _apply_listable_rules(cls, obj, rules):
        for i in rules:
            if i in obj:
                del obj[i]
        return obj
