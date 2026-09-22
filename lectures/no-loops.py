# Given two arrays [a1, ..., aN] and [b1, ..., bN], print all (ai, bj) such that ai*bj > 25
from functools import reduce
import timeit
import itertools

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

# This filters out all pairs with product <= 25
bigmuls = lambda xs, ys: [x_y for x_y in combine(xs,ys) if x_y[0]*x_y[1] > 25]
# This builds pairs of the list[x, y, z, x, y, z, x, y, z, ...] and the result of dupelms
combine = lambda xs, ys: itertools.zip_longest(xs*len(ys), dupelms(ys,len(xs)))
# This takes lst = [a, b, c] and produces [a, ..., a, b, ..., b, c, ..., c] with each element repeated n times
dupelms = lambda lst, n: reduce( lambda s, t: s+t, list(map(lambda l,n=n: [l]*n, lst)))

print(pairs(a, b))
print(betterpairs(a, b))
print(funcpairs(a, b))
print(bigmuls(a, b))

print(timeit.timeit(lambda: pairs(a, b), number=100_000))
print(timeit.timeit(lambda: betterpairs(a, b), number=100_000))
print(timeit.timeit(lambda: funcpairs(a, b), number=100_000))
print(timeit.timeit(lambda: bigmuls(a, b), number=100_000))