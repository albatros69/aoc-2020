#! /usr/bin/env python

import sys

def convert_to_decimal(val, conv):
    result=0
    for c in val:
        result = 2*result+conv[c]
    return result

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

result=0
seat_ids = []

for l in lines:
    row = convert_to_decimal(l[:7], { 'F': 0, 'B': 1})
    col = convert_to_decimal(l[7:10], { 'L': 0, 'R': 1})
    seat_id = 8*row+col
    # Part 1
    result = max(result, seat_id)
    seat_ids.append(seat_id)

print(result)

# Part 2
for s in seat_ids:
    if s+1 not in seat_ids and s+2 in seat_ids:
        print(s+1)
        break
