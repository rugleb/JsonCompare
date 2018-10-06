from abc import ABC


class Error(ABC):
    expected = None
    received = None

    template = 'Expected: <{e}>, received: <{r}>'

    def __init__(self, expected, received):
        self.expected = expected
        self.received = received

    def message(self):
        msg = self.template.format(e=self.expected, r=self.received)
        return msg

    def report(self):
        return {
            '_message': self.message(),
            '_expected': self.expected,
            '_received': self.received,
        }


class TypesNotEqual(Error):
    template = 'Types not equal. Expected: <{e}>, received: <{r}>'
