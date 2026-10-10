from itertools import product, tee, islice, count, permutations
from collections.abc import Iterator
from fractions import Fraction
from math import gcd


def Monoid(S, op, i):
    is_iterator = isinstance(S, Iterator)
    S = tee(S)[0]  # Every new instance of __inner should work on a different copy of S

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

        _assertions = {**Base._assertions, check_invertibility: "Invertibility"}

    return __inner


def AbellianGroup(S, op, i):
    Base = Group(S, op, i)

    class __inner(Base):

        def check_commutativity(self):
            return all(
                self._op(a, b) == self._op(b, a) for a, b in product(self._A, repeat=2)
            )

        _assertions = {**Base._assertions, check_commutativity: "Commutativity"}

    return __inner


def Ring(S, add, mul, zero, one):

    class __inner:

        def __init__(self):
            if isinstance(S, Iterator):
                S_add, S_mul = tee(S)
            else:
                S_add = S_mul = S
            self._g = AbellianGroup(S_add, add, zero)()
            self._m = Monoid(S_mul, mul, one)()
            self.validate()

        @property
        def _add(self):
            return self._g._op

        @property
        def _mul(self):
            return self._m._op

        @property
        def _A(self):
            return self._g._A.union(self._m._A)

        def validate(self):
            self._g.validate()
            self._m.validate()
            for f, name in self._assertions.items():
                assert f(self), f"{name} is not satisfied"

        def check_distributivity(self):
            return all(
                self._mul(a, self._add(b, c))
                == self._add(self._mul(a, b), self._mul(a, c))
                and self._mul(self._add(a, b), c)
                == self._add(self._mul(a, c), self._mul(b, c))
                for a, b, c in product(self._A, repeat=3)
            )

        _assertions = {check_distributivity: "Distributivity"}

    return __inner


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


# --- MONOIDS ---

# Boolean OR
BoolsMonoid = Monoid(
    S={True, False},
    op=lambda a, b: a or b,
    i=False,
)

# Z_n under modular addition
ZNMonoid = lambda n: Monoid(
    S=range(n),
    op=lambda a, b: (a + b) % n,
    i=0,
)


# --- GROUPS ---

# Permutations of RGB under composition
def compose(p, q):
    symbols = "RGB"
    return tuple(p[symbols.index(x)] for x in q)


RGBGroup = Group(
    S=list(permutations("RGB")),
    op=compose,
    i=("R", "G", "B"),
)

# Q \ {0} under multiplication
RationalGroup = Group(
    S=rationals(),
    op=lambda a, b: a * b,
    i=Fraction(1),
)

WrongGroup = Group(
    S={0, 1, 2},
    op=lambda a, b: a * b,
    i=1,
)


# --- RINGS ---

# Trivial ring {0}
TrivialRing = Ring(
    S={0},
    add=lambda a, b: a + b,
    mul=lambda a, b: a * b,
    zero=0,
    one=0,
)

# Integers Z under addition and multiplication
IntegerRing = Ring(
    S=integers(withzero=True),
    add=lambda a, b: a + b,
    mul=lambda a, b: a * b,
    zero=0,
    one=1,
)

# Z4 under modular addition and multiplication
Z4Ring = Ring(
    S=range(4),
    add=lambda a, b: (a + b) % 4,
    mul=lambda a, b: (a * b) % 4,
    zero=0,
    one=1,
)


# ============================================================
# TEST RUNNER
# ============================================================


def test(name, factory):
    try:
        factory()
        print(f"[PASS] {name}")
    except AssertionError as e:
        print(f"[FAIL] {name}: {e}")
    except Exception as e:
        print(f"[ERROR] {name}: {type(e).__name__}: {e}")


if __name__ == "__main__":

    print("\nMONOIDS")
    test("Boolean OR", BoolsMonoid)
    test("Z3 addition", ZNMonoid(3))
    test("Z4 addition", ZNMonoid(4))
    test("Z30 addition", ZNMonoid(30))

    print("\nGROUPS")
    test("RGB permutations", RGBGroup)
    test("Nonzero rationals multiplication", RationalGroup)
    test("Wrong group", WrongGroup)

    print("\nRINGS")
    test("Trivial ring {0}", TrivialRing)
    test("Integer ring Z", IntegerRing)
    test("Ring Z4", Z4Ring)
