import sys
import math
from itertools import islice


def evenfacts():
    """Generator of factorial numbers in even positions of the sequence"""
    a, x = 1, 2
    while True:
        yield a
        a *= x
        x += 1
        a *= x
        x += 1


def signs():
    """Generator of alternating 1 and -1"""
    a = 1
    while True:
        yield a
        a *= -1


def evens():
    """Generator of even numbers, from 1"""
    a = 1
    while True:
        yield a
        a += 2


def sin_taylor_terms(x):
    """Generator of terms of the taylor's series for sin(x)"""
    calc = lambda fact, sign, exp: sign * x**exp / fact
    for f, s, e in zip(evenfacts(), signs(), evens()):
        yield calc(f, s, e)


x, n = float(sys.argv[1]), int(sys.argv[2])

libsol = math.sin(x)
mysol = sum(islice(sin_taylor_terms(x), n))
print(f"Mine: {mysol}")
print(f"Libs: {libsol}")
print(f"Diff: {abs(libsol - mysol):.3E}")