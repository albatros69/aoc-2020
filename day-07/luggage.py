#! /usr/bin/env python

import sys
import re
from collections import defaultdict

lines = []
for line in sys.stdin:
	lines.append(line.rstrip('\n'))


# Part 1
def find_parent_bags(color, rules):
    result = set()
    for r in rules:
        if color in rules[r].keys():
            result.add(r)
            result.update(find_parent_bags(r, rules))
    return result

# Part 2
def count_child_bags(color, rules):
    return 1 + sum(v*count_child_bags(c, rules) for (c, v) in rules[color].items())


rules = defaultdict(dict)
content_re = re.compile("^(?P<nb>[0-9]+) (?P<color>[a-z ]+) bag.*$")
for l in lines:
    color, contents = l.split(' bags contain ')
    for content in contents.split(', '):
        if content.startswith('no'):
            rules[color] = {}
        else:
            m = content_re.match(content)
            rules[color][m.group('color')] = int(m.group('nb'))

# Part 1
print(len(find_parent_bags('shiny gold', rules)))

# Part 2
print(count_child_bags('shiny gold', rules) -1)
# "-1" to remove the shiny gold bag that contains everything

