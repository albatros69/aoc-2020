#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def transform(subject, loop_size, seed=1):
    result=seed
    for _ in range(loop_size):
        result=(result*subject)%20201227
    return result

# print(transform(7, 8))
# print(transform(7,11))

def reverse_pubk(pubk):
    loop_size = 1
    tentative = transform(7, loop_size)
    while tentative != pubk:
        tentative = transform(7, 1, seed=tentative)
        loop_size+=1
    return loop_size

# print(reverse_pubk(transform(7, 8)))
# print(reverse_pubk(transform(7,11)))

loop_size=reverse_pubk(int(lines[0]))
enc_key=transform(int(lines[1]), loop_size)

print(enc_key)
