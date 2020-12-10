#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(int(line.rstrip('\n')))

adapters = sorted(lines) # we sort the lines by ascending rate

# Part 1
output=0
differences=dict.fromkeys(range(4), 0)
differences[3] = 1 # to account for the device's built-in adapter

for rate in adapters:
    if rate-output<=3:
        differences[rate-output] += 1
        output=rate
    else:
        raise ValueError

print(differences, differences[1]*differences[3])

# Part 2
extended_adapters=[0]+adapters+[adapters[-1]+3]

cache = dict()
def search_solutions_rec(l):
    if len(l) <= 2:
        return 1
    else:
        a,_,c, *tail = l
        if c-a <= 3: # we can skip the value between a & c
            if (a,c) not in cache: # we didn't already compute that
                tmp1, tmp2 = search_solutions_rec([a,c]+tail), search_solutions_rec(l[1:])
                cache[(a,c)] = tmp1 + tmp2
            return cache[(a,c)]
        else: # we can skip a and continue
            return search_solutions_rec(l[1:])

print(search_solutions_rec(extended_adapters))
