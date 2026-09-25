# 1)
def identity(n):
    return [[1 if r == c else 0 for c in range(0, n)] for r in range(0, n)]


print(identity(5))


# 2)
def square(n):
    return [[r * n + c for c in range(1, n + 1)] for r in range(0, n)]


print(square(5))


# 3)
def transpose(A):
    return [[A[c][r] for c in range(0, len(A))] for r in range(0, len(A[0]))]


print(transpose([[1, 2, 3], [4, 5, 6]]))


# 4)
def multiply(A, B):
    elem = lambda r, c: sum(A[r][k] * B[k][c] for k in range(0, len(A[0])))

    return [[elem(r, c) for c in range(0, len(B[0]))] for r in range(0, len(A))]


A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8], [9, 10], [11, 12]]

print(multiply(A, B))
print(multiply(B, A))
