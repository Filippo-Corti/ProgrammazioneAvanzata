alkaline_earth_metals = [
    (56, 'Barium'),
    (4, 'Beryllium'),
    (20, 'Calcium'),
    (12, 'Magnesium'),
    (88, 'Radium'),
    (38, 'Strontium')
]

# 1)
print(max(alkaline_earth_metals, key=lambda p: p[0])[0])

# 2)
alksort = sorted(
    alkaline_earth_metals,
    key=lambda p: p[0]
)
print(alksort)

# 3)
alkdict = {p[1]: p[0] for p in alkaline_earth_metals}
print(alkdict)

# 4)
noble_gases = [
    (2, 'Helium'),
    (10, 'Neon'),
    (18, 'Argon'),
    (36, 'Krypton'),
    (54, 'Xenon'),
    (86, 'Radon')
]
nobledict = {p[1]: p[0] for p in noble_gases}
print(nobledict)

# 5)
print(sorted([
    p for p in (nobledict | alkdict).items()
], key=lambda p: p[0]))
