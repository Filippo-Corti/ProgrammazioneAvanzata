import sys
import re
from collections import Counter


def freq(filename, n):
    """Returns the list of words that appear more than n times in the file, with their frequencies"""
    with open(filename) as f:
        getwords = lambda: re.split(r"\W+", f.read())[:-1]
        listtocounter = lambda l: Counter(w.lower() for w in l)
        sortdictbyval = lambda d, reverse: sorted(
            d.items(), key=lambda p: p[1], reverse=reverse
        )
        return [
            (word, count)
            for word, count in sortdictbyval(listtocounter(getwords()), reverse=True)
            if count > n
        ]


print(freq(sys.argv[1], int(sys.argv[2])))
