#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


mandatory_keys = ( 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', ) # 'cid',
def passport_is_valid(p):
    # Part 1:
    # return all([ k in p.keys() for k in mandatory_keys ])

    # Part 2:
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    # cid (Country ID) - ignored, missing or not.

    tests = []
    for k,v in p.items():
        if k=='byr':
            tests.append(len(v)==4 and v.isdigit() and 1920<=int(v)<=2002)
        elif k=='iyr':
            tests.append(len(v)==4 and v.isdigit() and 2010<=int(v)<=2020)
        elif k=='eyr':
            tests.append(len(v)==4 and v.isdigit() and 2020<=int(v)<=2030)
        elif k=='hgt':
            tests.append((v.endswith('cm') and 150<=int(v[:-2])<=193) or
                         (v.endswith('in') and 59<=int(v[:-2])<=76))
        elif k=='hcl':
            tests.append(v[0]=='#' and len(v)==7 and all([ c in '0123456789abcdef' for c in v[1:] ]))
        elif k=='ecl':
            tests.append(v in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth',))
        elif k=='pid':
            tests.append(len(v)==9 and v.isdigit())

    # All mandatory keys are present and all tests passed
    return len(tests)==7 and all(tests)


passports = []
passport = {}
for l in lines:
    if l:
        for field in l.split():
            k,v = field.split(':')
            passport[k]=v
    else:
        passports.append(passport)
        passport = {}

# To no forget the last one, in case there was no empty trailing line
if len(passport)>0:
    passports.append(passport)

c = 0
for p in passports:
    if passport_is_valid(p): c+=1
print(c)