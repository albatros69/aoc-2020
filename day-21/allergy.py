#! /usr/bin/env python

import sys
import re
from collections import defaultdict
from functools import reduce
from copy import deepcopy


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

re_ingredients = re.compile(r"(?P<ingredients>[a-z ]+) \(contains (?P<allergens>.+)\)$")
products = []
allergens = defaultdict(list)
ingredients = defaultdict(set)
for l in lines:
    m=re_ingredients.match(l)
    ingre, allerg = m.group('ingredients').split(' '), m.group('allergens').split(', ')
    products.append((ingre, allerg))
    for i in ingre:
        ingredients[i] = ingredients[i].union(allerg)
    for a in allerg:
        allergens[a].append(set(ingre))

tmp = [ (reduce(lambda x,y: x&y, allergens[a]), a) for a in allergens ]
result = deepcopy(ingredients)
while len(tmp)>0:
    inter, allerg = min(tmp, key=lambda x:len(x[0]) )
    if len(inter)==1:
        tmp.remove((inter,allerg))
        for i in result:
            if i not in inter:
                result[i].discard(allerg)
        for i,(a,b) in enumerate(tmp):
            tmp[i] = (a.difference(inter), b)
    else:
        break

# Part 1
print(sum(sum(i in product for product,_ in products) for i in result if len(result[i])==0))
# Part 2
tmp = [ (result[i].pop(), i) for i in result if len(result[i])==1 ]
tmp.sort()
print(",".join(t[1] for t in tmp))



