from jsoncompare.errors import ValuesNotEqual


class Diff:

    @classmethod
    def compare(cls, e, a):
        return e == a

    @classmethod
    def diff(cls, e, a):
        if cls.compare(e, a):
            return {}
        return ValuesNotEqual(e, a)


class Float(Diff):
    pass


class Int(Diff):
    pass


class Str(Diff):
    pass


class Bool(Diff):
    pass


class Dict(Diff):
    pass


class List(Diff):
    pass
