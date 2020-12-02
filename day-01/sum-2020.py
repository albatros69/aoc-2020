#! /usr/bin/env python

import sys
from itertools import combinations

lines = []
for line in sys.stdin:
	lines.append(int(line.rstrip('\n')))

for (a,b) in combinations(lines, 2):
    if a+b == 2020:
        print(a,b,a*b)
        break

for (a,b,c) in combinations(lines, 3):
    if a+b+c == 2020:
        print(a,b,c,a*b*c)
        break
