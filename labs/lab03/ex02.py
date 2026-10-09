from itertools import product, tee, islice
from collections.abc import Iterator


def Monoid(S, op, i):
    is_iterator = isinstance(S, Iterator)
    S = tee(S)[0] # This makes it so that every new instance of __inner has a different copy of S to work on

    class __inner:

        # N is the size of the finite subset on which I check properties, if S is given as an iterator.
        # To check closure, I cannot simply assume that if an element is not in N, it is not in S.
        # To try a little more, I consider M values instead. If I put more assumptions on S, I could find M in a smarter way.
        N = 10
        M = 20

        def __init__(self):
            self.__original = tee(S)[0]
            self.__op = op
            self.__i = i

            if is_iterator:
                self.__A = set(islice(self.__S(), self.N))
                self.__B = set(islice(self.__S(), self.M))
            else:
                self.__A = set(self.__S())
                self.__B = set(self.__S())

            self.validate()

        def __S(self):
            self.__original, copy = tee(self.__original)
            return copy

        def validate(self):
            for f, name in self.assertions.items():
                assert f(self), f"{name} is not satisfied"

        def check_identity(self):
            if self.__i not in self.__A:
                return False
            return all(
                self.__op(a, self.__i) == a and self.__op(self.__i, a) == a
                for a in self.__A
            )

        def check_closure(self):
            return all(
                self.__op(a, b) in self.__B for a, b in product(self.__A, repeat=2)
            )

        def check_associativity(self):
            return all(
                self.__op(a, self.__op(b, c)) == self.__op(self.__op(a, b), c)
                for a, b, c in product(self.__A, repeat=3)
            )

        assertions = {
            check_identity: "Identity",
            check_closure: "Closure",
            check_associativity: "Associativity",
        }

    return __inner


BoolsMonoid = Monoid(S={True, False}, op=lambda a, b: a or b, i=False)
WrongMonoid = Monoid(S={0, 1, 2}, op=lambda a, b: a, i=0)
ZNMonoid = lambda n: Monoid(S=iter(range(n)), op=lambda a, b: (a + b) % n, i=0)

SumMonoid1 = Monoid(S=range(100), op=lambda a, b: (a + b) % 100, i=0)
SumMonoid2 = Monoid(S=iter(range(100)), op=lambda a, b: (a + b) % 100, i=0)

if __name__ == "__main__":
    m = BoolsMonoid()
    # m2 = WrongMonoid()
    # m3 = ZNMonoid(n=3)
    # m3 = ZNMonoid(n=30)
    sm1 = SumMonoid1()
    sm2 = SumMonoid2()
