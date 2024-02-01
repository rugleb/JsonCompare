from abc import ABC


class Error(ABC):
    expected = None
    received = None

    template = 'Expected: <{e}>, received: <{r}>'

    def __init__(self, expected, received):
        self.expected = expected
        self.received = received

    @property
    def message(self):
        msg = self.template.format(e=self.expected, r=self.received)
        return msg

    def explain(self):
        return {
            '_message': self.message,
            '_expected': self.expected,
            '_received': self.received,
        }


class TypesNotEqual(Error):
    template = 'Types not equal. Expected: <{e}>, received: <{r}>'

    def __init__(self, e, a):
        e = type(e).__name__
        a = type(a).__name__
        super().__init__(e, a)


class ValuesNotEqual(Error):
    template = 'Values not equal. Expected: <{e}>, received: <{r}>'


class KeyNotExist(Error):
    template = 'Key does not exist. Expected: <{e}>'


class LengthsNotEqual(Error):
    template = 'Lengths not equal. Expected <{e}>, received: <{r}>'


class ValueNotFound(Error):
    template = 'Value not found. Expected <{e}>'


class UnexpectedKey(Error):
    template = 'Unexpected key. Received: <{r}>'
