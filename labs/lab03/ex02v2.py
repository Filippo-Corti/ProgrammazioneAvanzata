from itertools import product, tee, islice
from collections.abc import Iterator


class Monoid:

    N = 10
    M = 200

    def __init__(self, S, op, i):
        is_iterator = isinstance(S, Iterator)

        self.__original = tee(S)[0]
        self._op = op
        self._i = i

        if is_iterator:
            self._A = set(islice(self._S(), self.N))
            self._B = set(islice(self._S(), self.M))
        else:
            self._A = set(self._S())
            self._B = set(self._S())

        self.validate()

    def _S(self):
        self.__original, copy = tee(self.__original)
        return copy

    def validate(self):
        for f, name in self._assertions.items():
            assert f(self), f"{name} is not satisfied"

    def check_identity(self):
        if self._i not in self._A:
            return False

        return all(
            self._op(a, self._i) == a
            and self._op(self._i, a) == a
            for a in self._A
        )

    def check_closure(self):
        return all(
            self._op(a, b) in self._B
            for a, b in product(self._A, repeat=2)
        )

    def check_associativity(self):
        return all(
            self._op(a, self._op(b, c))
            == self._op(self._op(a, b), c)
            for a, b, c in product(self._A, repeat=3)
        )

    _assertions = {
        check_identity: "Identity",
        check_closure: "Closure",
        check_associativity: "Associativity",
    }


class Group(Monoid):

    def check_invertibility(self):
        return all(
            any(
                self._op(a, b) == self._i
                and self._op(b, a) == self._i
                for b in self._B
            )
            for a in self._A
        )

    _assertions = {
        **Monoid._assertions,
        check_invertibility: "Invertibility",
    }


class AbelianGroup(Group):

    def check_commutativity(self):
        return all(
            self._op(a, b) == self._op(b, a)
            for a, b in product(self._A, repeat=2)
        )

    _assertions = {
        **Group._assertions,
        check_commutativity: "Commutativity",
    }


class Ring:

    def __init__(self, S, add, mul, zero, one):
        if isinstance(S, Iterator):
            # Keep a reference at the beginning of the iterator.
            S = tee(S)[0]
            S_add, S_mul = tee(S)
        else:
            S_add = S_mul = S

        self._g = AbelianGroup(S_add, add, zero)
        self._m = Monoid(S_mul, mul, one)

        self.validate()

    @property
    def _add(self):
        return self._g._op

    @property
    def _mul(self):
        return self._m._op

    @property
    def _A(self):
        return self._g._A

    def validate(self):
        self._g.validate()
        self._m.validate()

        for f, name in self._assertions.items():
            assert f(self), f"{name} is not satisfied"

    def check_distributivity(self):
        return all(
            self._mul(a, self._add(b, c))
            == self._add(self._mul(a, b), self._mul(a, c))
            and
            self._mul(self._add(a, b), c)
            == self._add(self._mul(a, c), self._mul(b, c))
            for a, b, c in product(self._A, repeat=3)
        )

    _assertions = {
        check_distributivity: "Distributivity",
    }