# Tail-recursion = the recursive call is the very last thing the function does

def echo():
    while True:
        x = input()
        print(x)
        if x == 'quit': 
            return
        
def rececho():
    x = input()
    print(x)
    if x != 'quit':
        rececho()
        
#rececho()


# Python does not perform tail recursion optimization. We shall do it by hand:

def fact(n): # Not tail-recursive
    if n == 1:
        return 1
    return n*fact(n-1)

def tailfact(n, acc=1): # Tail-recursive
    if n == 0:
        return acc
    return tailfact(n-1, acc*n)

# Idk how to do it by hand yet...

print(fact(4))
print(fact(4))

