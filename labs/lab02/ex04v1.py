from functools import reduce, lru_cache
import itertools
from math import isqrt


def divisors(n):
    firsthalf = [d for d in range(1, isqrt(n) + 1) if n % d == 0]
    secondhalf = [
        n // d for d in firsthalf[::-1] if d * d != n
    ]  # special case for sqrt(n)
    return itertools.chain(firsthalf, secondhalf)


def isprime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))


def ispractical(n):
    registernew = lambda l, n: [
        el or (i - n >= 0 and l[i - n]) for i, el in enumerate(l)
    ]
    l = [True] + [False] * n
    return all(reduce(registernew, divisors(n), l))


def arepractical(*ints):
    return all(map(ispractical, ints))


def issexypair(a, b):
    return (
        b - a == 6
        and isprime(a)
        and isprime(b)
        and all(not isprime(i) for i in range(a + 1, b))
    )


def istriplepair(a, b, c, e):
    return issexypair(a, b) and issexypair(b, c) and issexypair(c, e)


def isengineersparadise(n):
    return istriplepair(n - 9, n - 3, n + 3, n + 9) and arepractical(
        n - 8, n - 4, n, n + 4, n + 8
    )


def engineersparadises():
    for i in itertools.count():
        print(i)
        if isengineersparadise(i):
            yield i


if __name__ == "__main__":
    print(list(itertools.islice(engineersparadises(), 4)))
