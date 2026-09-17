def isprime(n):
    divs = [i for i in range(2, int(n**0.5)+1) if n%i==0]
    return len(divs) == 0

print(isprime(13))
print(isprime(25))

def isprimetoo(n):
    def monad(x):
        raise Exception("Not prime")

    try:
        [monad(i) for i in range(2, int(n**0.5)+1) if n%i==0]
        return True
    except:
        return False


print(isprimetoo(13))
print(isprimetoo(25))
