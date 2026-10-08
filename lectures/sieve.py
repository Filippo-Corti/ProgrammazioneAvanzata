from itertools import count
from collections import defaultdict



class Sieve:

    def __init__(self, N):
        self.__N = N
        self.__mem = bytearray(b"\x01") * (N + 1)
        self.__mem[0:2] = b"\x00\x00"

    def __iter__(self):
        self.__n = 1
        return self

    def __next__(self):
        for i in range(self.__n + 1, self.__N + 1):
            if self.__mem[i]:
                self.__n = i
                break
        else:
            raise StopIteration

        for i in range(self.__n**2, self.__N + 1, self.__n):
            self.__mem[i] = 0
        return self.__n


sieve = Sieve(100)
for prime in sieve:
    print(prime)

# --- Easy way for infinite primes ---

def infinite_primes():
    # For each non-prime number, we store which primes have flagged it as non-prime
    composites = defaultdict(list)

    for n in count(2):
        if n not in composites:
            yield n # Nobody flagged n -> it's prime
            composites[n * n] = [n] # First flag for n is n*n
        else:
            for p in composites[n]: # If p flagged n, then n+p should also be flagged
                composites[n + p].append(p)


for prime in infinite_primes():
    print(prime)
