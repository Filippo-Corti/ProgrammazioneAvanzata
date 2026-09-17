# Tower of Hanoi:
# 3 rods, n disks stacked on the 1st rod
# goal is to move all disks on the 3rd rod
# you can only place a disk on a larger disk

def free_rod(from_rod, to_rod):
    return 3 - from_rod - to_rod

def hanoi(rods, how_many, from_rod, to_rod):
    """Move how_many disks from from_rod to to_rod"""
    if how_many > 1:
        hanoi(rods, how_many-1, from_rod, free_rod(from_rod, to_rod))   
    d = rods[from_rod].pop()
    rods[to_rod].append(d)
    if how_many > 1:
        hanoi(rods, how_many-1, free_rod(from_rod, to_rod), to_rod)    
    return
        
n = 10
rods = [[i for i in range(n, 0, -1)], [], []]

print(rods)
hanoi(rods, n, 0, 2)
print(rods)