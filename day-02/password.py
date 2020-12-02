#! /usr/bin/env python

import sys
from re import split
from collections import Counter

lines = []
for line in sys.stdin:
	lines.append(line.rstrip('\n'))

valid=0
for l in lines:
    (i,s,c,pwd) = split("[ :-]+", l)
    # count = Counter(pwd)
    # if int(i) <= count[c] <= int(s):
    #     valid += 1
    if (pwd[int(i)-1] == c and pwd[int(s)-1] != c) or (pwd[int(i)-1] != c and pwd[int(s)-1] == c):
        valid +=1

print(valid)