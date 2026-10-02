import sys
import math
from itertools import islice, cycle, count


def evenfacts():
    """Generator of factorial numbers in even positions of the sequence"""
    a, x = 1, 2
    while True:
        yield a
        a = (a * x) * (x + 1)
        x += 2


signs = lambda: cycle([1, -1])  # Generates 1, -1, 1, -1, ...
odds = lambda: count(start=1, step=2)  # Generates 1, 3, 5, ...


def sin_taylor_terms(x):
    """Generator of terms of the taylor's series for sin(x)"""
    calc = lambda fact, sign, exp: sign * x**exp / fact
    for f, s, e in zip(evenfacts(), signs(), odds()):
        yield calc(f, s, e)


x, n = float(sys.argv[1]), int(sys.argv[2])

libsol = math.sin(x)
mysol = sum(islice(sin_taylor_terms(x), n))
print(f"Mine: {mysol}")
print(f"Libs: {libsol}")
print(f"Diff: {abs(libsol - mysol):.3E}")
