# Given two arrays [a1, ..., aN] and [b1, ..., bN], print all (ai, bj) such that ai*bj > 25
from functools import reduce
import timeit

a = [1, 2, 3, 4]
b = [10, 11, 12, 13]

def pairs(a, b):
    c = list()
    for ai in a:
        for bi in b:
            if ai*bi > 25:
                c.append((ai, bi))
    return c

def betterpairs(a, b):
    return [(ai, bi) for ai in a for bi in b if ai*bi > 25]

def funcpairs(a, b):
    return list(filter(
        lambda pair: pair[0]*pair[1]>25,
        zip(
            a*len(b), 
            reduce(
                lambda acc, x: acc+x,
                [[bi]*len(a) for bi in b],
            ) 
        )
    ))

print(pairs(a, b))
print(betterpairs(a, b))
print(funcpairs(a, b))

print(timeit.timeit(lambda: pairs(a, b), number=100_000))
print(timeit.timeit(lambda: betterpairs(a, b), number=100_000))
print(timeit.timeit(lambda: funcpairs(a, b), number=100_000))