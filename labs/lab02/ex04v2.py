import sympy
import sys
from operator import mul
from functools import reduce

sys.setrecursionlimit(10**8)


def primegen():
    p = 1
    while True:
        p = sympy.nextprime(p)
        yield p


def factorize(n):
    primes = primegen()
    factors = []
    p = next(primes)

    while p * p <= n:
        if n % p == 0:
            if factors and factors[-1][0] == p:
                factors[-1] = (p, factors[-1][1] + 1)
            else:
                factors.append((p, 1))
            n //= p
        else:
            p = next(primes)

    if n > 1:
        factors.append((n, 1))

    return factors

def ispractical(n):
    factors = factorize(n)

    def checkprime(i):
        return factors[i][0] <= 1 + reduce(
            mul,
            (
                (factors[j][0] ** (factors[j][1] + 1) - 1) // (factors[j][0] - 1)
                for j in range(i)
            ),
            1,
        )

    return all((checkprime(i) for i in range(len(factors))))


def triplepairgen():
    previous = None
    run = []

    for p in primegen():
        if not previous or p != previous + 6:
            run = [p]
        else:
            run.append(p)

        if len(run) == 4:
            yield run.copy()
            run.pop(0)

        previous = p


def engineersparadises():
    for triplepair in triplepairgen():
        n = triplepair[1] + 3
        if all(ispractical(n + i) for i in {-8, -4, 0, 4, 8}):
            yield n


g = engineersparadises()
for i in range(4):
    print(f"--------- {next(g)} ----------")

# First: 219869980
#
