# HAWAII +
#  IDAHO +
#   IOWA +
#   OHIO =
# STATES

# Letters = HAWIODSTE
# Numbers = 0123456789

# I + 0 + A + 0 = aS
# I + H + W + I + a = bE
# A + A + O + H + b = cT
# W + D + I + O + c = dA
# A + I + d = eT
# H + e = S

import re
from itertools import permutations
from functools import reduce


def evalword(word, mapping):
    return reduce(lambda acc, x: acc * 10 + mapping[x], word, 0)


puzzle = "HAWAII + IDAHO + IOWA + OHIO = STATES"
words = re.findall(r"[A-Z]+", puzzle)
inputs, output = words[:-1], words[-1]
firstletters = set(w[0] for w in inputs)
letters = set("".join(words))
digits = "0123456789"

for perm in permutations(digits):
    mapping = {letter: int(digit) for letter, digit in zip(letters, perm)}
    if any(mapping[fl] == 0 for fl in firstletters): continue
    if sum((evalword(w, mapping) for w in inputs)) == evalword(output, mapping):
        translation = str.maketrans({l: str(d) for l, d in mapping.items()})
        print(puzzle)
        print(puzzle.translate(translation))
        break
