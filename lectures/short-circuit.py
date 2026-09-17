# Short-circuiting:
# Note that the result is always the last evaluated operand, not necessarily a boolean.

# AND short-circuits when the first operand is False.

x = 1
print((x==1) and 'one') # 'one'

x = 2
print((x==1) and 'one') # 'False'

x = 1
print('one' and (x==1)) # 'True'

x = 5
print(True and 'one' and '' and x==1 and 'two') # ''


# OR short-circuits when the first operand is True.

x = 3
print((x==3) or 'one') # True

x = 3
print('one' or (x==3)) # 'one'

# -------
print("---------")

a = 2
if a % 2 == 0:
    res = 'even'
else:
    res = 'odd'
print(res)

res = 'even' if a%2==0 else 'odd'
print(res)

res = ((a%2==0) and 'even') or 'odd'
print(res)

# -------
print("--------")

a = 3
if a % 2 == 0:
    print('even')
else:
    print('odd')

print(a%2==0 and 'even' or 'odd')


