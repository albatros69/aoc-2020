#! /usr/bin/env python

import sys
from re import split
from collections import Counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

valid_part1, valid_part2=0,0
for l in lines:
    (i,s,c,pwd) = split("[ :-]+", l)

    # Part 1
    count = Counter(pwd)
    if int(i) <= count[c] <= int(s):
        valid_part1 += 1
    # Part 2
    if (pwd[int(i)-1] == c and pwd[int(s)-1] != c) or (pwd[int(i)-1] != c and pwd[int(s)-1] == c):
        valid_part2 +=1

print("Part 1:", valid_part1, "\nPart 2:", valid_part2)
