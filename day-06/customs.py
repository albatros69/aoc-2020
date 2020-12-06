#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
	lines.append(line.rstrip('\n'))

# Part 1
# answers = set()
# Part 2
answers = set('abcdefghijklmnopqrstuvwxyz') # set([ chr(c) for c in range(ord('a'), ord('z')+1) ])
yes_count = []
for l in lines:
    if l:
        # answers = answers.union(set(l))
        answers = answers.intersection(set(l))
    else:
        yes_count.append(len(answers))
        # answers = set()
        answers = set('abcdefghijklmnopqrstuvwxyz')

if len(answers) > 0:
    yes_count.append(len(answers))

print(yes_count, sum(yes_count))