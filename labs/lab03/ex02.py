from itertools import product, tee, islice, count, permutations
from collections.abc import Iterator
from fractions import Fraction
from math import gcd


def integers(withzero=False):
    if withzero:
        yield 0
    n = 1
    while True:
        yield n
        yield -n
        n += 1


def rationals(withzero=False):
    if withzero:
        yield Fraction(0)
    for n in count(2):
        for p in range(1, n):
            q = n - p
            if gcd(p, q) == 1:
                yield Fraction(p, q)
                yield Fraction(-p, q)


def Monoid(S, op, i):
    is_iterator = isinstance(S, Iterator)
    S = tee(S)[
        0
    ]  # This makes it so that every new instance of __inner has a different copy of S to work on

    class __inner:

        # N is the size of the finite subset on which I check properties, if S is given as an iterator.
        # To check closure, I cannot simply assume that if an element is not in N, it is not in S.
        # To try a little more, I consider M values instead. If I put more assumptions on S, I could find M in a smarter way.
        N = 10
        M = 200

        def __init__(self):
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
                self._op(a, self._i) == a and self._op(self._i, a) == a for a in self._A
            )

        def check_closure(self):
            return all(self._op(a, b) in self._B for a, b in product(self._A, repeat=2))

        def check_associativity(self):
            return all(
                self._op(a, self._op(b, c)) == self._op(self._op(a, b), c)
                for a, b, c in product(self._A, repeat=3)
            )

        _assertions = {
            check_identity: "Identity",
            check_closure: "Closure",
            check_associativity: "Associativity",
        }

    return __inner


def Group(S, op, i):
    Base = Monoid(S, op, i)

    class __inner(Base):

        def check_invertibility(self):
            return all(
                any(
                    self._op(a, b) == self._i and self._op(b, a) == self._i
                    for b in self._B
                )
                for a in self._A
            )

        assertions = {**Base._assertions, check_invertibility: "Invertibility"}

    return __inner


# --- Monoids ---
BoolsMonoid = Monoid(S={True, False}, op=lambda a, b: a or b, i=False)
WrongMonoid = Monoid(S={0, 1, 2}, op=lambda a, b: a, i=0)
ZNMonoid = lambda n: Monoid(S=iter(range(n)), op=lambda a, b: (a + b) % n, i=0)
SumMonoid1 = Monoid(S=range(100), op=lambda a, b: (a + b) % 100, i=0)
SumMonoid2 = Monoid(S=iter(range(100)), op=lambda a, b: (a + b) % 100, i=0)

# --- Groups ---
a = lambda t: (t[1], t[0], t[2])
b = lambda t: (t[0], t[2], t[1])
RGBGroup = Group(S=permutations("RGB"), op=lambda x: b(a(x)), i=("R", "G", "B"))  # ????

RationalGroup = Group(S=rationals(), op=lambda a, b: a * b, i=Fraction(1))

if __name__ == "__main__":
    sm1 = SumMonoid1()
    sm2 = SumMonoid2()

    RationalGroup()
