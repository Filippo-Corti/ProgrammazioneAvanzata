# Given two arrays [a1, ..., aN] and [b1, ..., bN], print all (ai, bi) such that ai*bi > 25

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
    

print(pairs(a, b))
