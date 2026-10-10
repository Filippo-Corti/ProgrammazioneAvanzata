from bisect import insort


class SortedDict(dict):

    def __init__(self, cmp):
        super().__init__()
        self.__keys = []

        class __Key:  # Alternatively to all of this, you can use sorted(iterable, key=functools.cmp_to_key(cmp)) exists.

            def __init__(self, v):
                self.__v = v
                self.__cmp = cmp

            def get(self):
                return self.__v

            def __lt__(self, other):
                return self.__cmp(self.__v, other.__v) < 0

            def __gt__(self, other):
                return self.__cmp(self.__v, other.__v) > 0

            def __eq__(self, other):
                return self.__cmp(self.__v, other.__v) == 0

        self.__Key = __Key

    def __setitem__(self, key, value):
        if key not in self:
            insort(self.__keys, self.__Key(key))  # insert + sort

        return super().__setitem__(key, value)

    def __delitem__(self, key):
        for i, otherkey in enumerate(self.keys()):
            if key is otherkey or (key == otherkey and hash(key) == hash(otherkey)):
                self.__keys.pop(i)
                return super().__delitem__(key)
        raise KeyError(key)

    def __iter__(self):
        return (key.get() for key in self.__keys)

    def items(self):
        return ((key, self[key]) for key in self)

    def keys(self):
        return (key for key in self)

    def values(self):
        return (self[key] for key in self)


def cmp(x, y):
    if isinstance(x, int) and not isinstance(y, int):
        return -1
    if not isinstance(x, int) and isinstance(y, int):
        return 1
    return 0


if __name__ == "__main__":

    d = SortedDict(cmp=cmp)
    d["test"] = "Hi"
    d[3] = 4

    d[3] = 5
    d["other"] = "Bye"
    d["hi"] = SortedDict(cmp=cmp)
    d[4] = 4

    del d[4]

    for k, v in d.items():
        print(k, v)
