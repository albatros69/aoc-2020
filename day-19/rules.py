#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Rule():
    character=''
    rules=None

    def __init__(self, line) -> None:
        if line.startswith('"'):
            self.character = line.strip('"')
        else:
            self.rules=tuple( tuple(int(a) for a in alternative.strip().split()) for alternative in line.strip().split('|'))

rules = dict()
while True:
    l = lines.pop(0)
    if not l:
        break
    else:
        i, line = l.split(':')
        rules[int(i)] = Rule(line.strip())

def flatten(id):
    """ Develop a rule into a list of all the possible strings """
    rule = rules[id]
    if rule.character:
        return rule.character
    elif rule.rules:
        result = []
        for r in rule.rules:
            accu = ['']
            for alternative in map(flatten, r):
                accu = [ a+b for a in accu for b in alternative ]
            result.extend(accu)
        return result

# Part 1
possible_strings = flatten(0)
result = 0
for l in lines:
    if l in possible_strings:
        result+=1
print(result)

# Part 2
# 0 is equal to 8 11, it develops to 42+ (42+ 31+) with a balanced number
# of 42s and 31s at the end.
# So we first eat all the 42s at the beginning, then 31s at the end
# but we need to have more 42s at the beginning than 31s at the end

thirtyone = flatten(31)
fortytwo = flatten(42)

def is_fortytwos(s):
    """ Count all 42s at the beginning. Return also the rest of the string """
    for test in fortytwo:
        if s.startswith(test):
            tmp, count, rest = is_fortytwos(s[len(test):])
            if tmp:
                return True, 1+count, s
            else:
                return False, 1+count, rest
    return False, 0, s

def is_thirtyones(s):
    """ Count all the 31s in the string till the end """
    for test in thirtyone:
        if s.startswith(test):
            if len(s)==len(test):
                return True, 1
            else:
                tmp, count = is_thirtyones(s[len(test):])
                if tmp:
                    return True, 1+count
                else:
                    return False, 1+count
    return False, 0

result = 0
for l in lines:
    _, count_42, rest = is_fortytwos(l)
    is_31, count_31 = is_thirtyones(rest)
    if is_31 and count_31<count_42:
        result += 1
print(result)

