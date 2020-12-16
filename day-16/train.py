#! /usr/bin/env python

import sys
import re
from collections import defaultdict
from functools import reduce

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

rules = dict()
re_rules = re.compile(r'^(?P<field>.+): (?P<bi1>[0-9]+)-(?P<bs1>[0-9]+) or (?P<bi2>[0-9]+)-(?P<bs2>[0-9]+)$')
while True:
    l = lines.pop(0)
    if l:
        m = re_rules.match(l)
        rules[m.group('field')] = ((int(m.group('bi1')), int(m.group('bs1'))),
                                   (int(m.group('bi2')), int(m.group('bs2'))), )
    else:
        break

lines.pop(0)
my_ticket = [ int(a) for a in lines.pop(0).split(',') ]

lines.pop(0); lines.pop(0)
tickets = [ [ int(a) for a in l.split(',') ] for l in lines ]

def is_valid(value, r1, r2):
    a,b = r1 ; c,d = r2
    return a <= value <= b or c <= value <= d

# Part 1
invalid = []
for t in tickets:
    invalid.extend([ v for v in t if not any(is_valid(v, *rule) for rule in rules.values()) ])

print(sum(invalid))

# Part 2
possible_result = defaultdict(list)
# For each position in the ticket, we look for the possible fields based on the nearby values
for i in range(len(my_ticket)):
    for field, rule in rules.items():
        if all(is_valid(ticket[i], *rule) for ticket in tickets if ticket[i] not in invalid):
            # if all the tickets are valid for this field, we store the position as a
            # candidate for this field
            possible_result[field].append(i)

result = {}
# We sort the possible results on the length of the candidates' list
for field in sorted(possible_result.keys(), key=lambda x: len(possible_result[x])):
    if len(possible_result[field]) == 1:
        # If there's only one value, we have our winner for this field.
        value = possible_result[field][0]
        result[field] = value
        # We then eliminate this position in all the remaining fields
        for f in possible_result:
            if f != field:
                try:
                    possible_result[f].remove(value)
                except:
                    pass
    else:
        print('Error, there are two solutions...')
        exit()

# for field in result:
#     print(f'{field}: {my_ticket[result[field]]}')

print(reduce(lambda x,y: x*y, (my_ticket[result[f]] for f in result if f.startswith('departure'))))
