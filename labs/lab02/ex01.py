from math import gcd, lcm
from operator import mul
from functools import reduce

# 1) Sum all natural numbers below 1000 that are multiples of 3 and 5
mult3and5 = lambda x: x % 3 == 0 and x % 5 == 0
print(f"1. {sum(filter(mult3and5, range(1000)))}")

## 2) Calculate the smallest number divisible by each of the numbers 1 to 20

# First solution: compute the LCM
mylcm = lambda a, b: (a * b) // gcd(a, b)
lcmall = lambda *ints: reduce(mylcm, ints)


# Second solution: build the factors by myself
def dividemults(vals, i):
    factor = vals[i]
    return vals[: i + 1] + [v // factor if not v % factor else v for v in vals[i + 1 :]]


vals = reduce(dividemults, range(20), list(range(1, 21)))

print(f"2. {lcm(*range(1, 21))} = {lcmall(*range(1, 21))} = {reduce(mul, vals)}")

# 3) Calculate the sum of the figures of 2^1000
digitsum = lambda n: sum(map(int, str(n)))
print(f"3. {digitsum(2**1000)}")


# 4) Calculate the first term in the Fibonacci sequence to contain 1000 digits
def genfib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


digitcount = lambda n: len(str(n))
print(f"4. {next(filter(lambda n: digitcount(n) >= 1000, genfib()))}")
