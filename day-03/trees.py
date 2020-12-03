#! /usr/bin/env python

import sys
from functools import reduce

lines = []
for line in sys.stdin:
	lines.append(line.rstrip('\n'))

# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.
strategy = [ (1, 1), (3, 1), (5, 1), (7, 1), (1, 2) ]
result = []

for (right, down) in strategy:
    trees = 0
    col = 0

    for l in lines[::down]:
        trees += 1 if l[col]=='#' else 0
        col = (col+right) % len(l)

    result.append(trees)

print(result, "-->", reduce(lambda x,y: x*y, result))
