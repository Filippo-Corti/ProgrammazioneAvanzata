from math import sqrt, floor, log10, ceil

PHI = (1 + sqrt(5)) / 2

# The Binet Formula can be used to compute the index of the first fibonacci number with at least X digits 
def firstfibindex(mindigits):
    if mindigits == 1: return 1
    return ceil((mindigits - 1 + log10(sqrt(5))) / log10(PHI))

# The same Binet Formula can be used to estimate the value of the n-th Fibonacci number
# (the formula is actually exact, but python arithmetics makes it only work for small n)
def nthfib(n):
    if n > 100: return -1
    varphi = (1 - sqrt(5)) / 2
    return (PHI**n - varphi**n) / sqrt(5)

# The fast-doubling algorithm can be used to compute the n-th fibonacci number in O(logn) time.
def nthfib_doubling(n):

    def doubling(k): # Returns (F(k) and F(k+1))
        if k == 0: return (0, 1)

        Fn, Fnp1 = doubling(k >> 1)
        F2n = Fn * (2*Fnp1 - Fn) # This is a known identity
        F2np1 = Fn**2 + Fnp1**2 # So is this

        if k % 2 == 0: # If k is even, then Fk = F2n
            return F2n, F2np1
        # If k is odd, then Fk = F2np1
        return F2np1, F2n + F2np1 

    return doubling(n)[0]

if __name__ == '__main__':
    print(nthfib_doubling(firstfibindex(1000)))

