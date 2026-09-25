import os

# 1)
def cat(filename):
    print(open(filename).read(), end="")

#cat('input.txt')

# 2)
def chmod(filename, mode):
    os.chmod(filename, mode)

chmod('input.txt', 0o700)

# 3)
def more(filename, n):
    with open(filename) as file:
        while True:
            content = ''.join(file.readline() for _ in range(n))
            if content == '': break
            print(content, end="")
            input("--------- PRESS ENTER ---------")


more('input.txt', 1)