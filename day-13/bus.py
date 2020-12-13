#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

timestamp=int(lines[0])
buses = [ int(b) for b in lines[1].split(',') if b!='x' ]

result=[]
for id in buses:
    result.append((id - timestamp%id, id))

# Part 1
wait_time, bus = min(result)
print(wait_time, bus, wait_time*bus)

# Part 2
# to test with test2, you can execute the following in your shell
# $ for line in `cat test2`; do (echo 0; echo $line) | python bus.py ; done

buses = [ (int(b), offset) for offset,b in enumerate(lines[1].split(',')) if b!='x' ]

def is_valid(tstamp):
    return all(( (tstamp+offset)%bus == 0 for bus,offset in buses))

# Naïve brute-froce approach that works for all the test cases
# tstamp=0
# bus, offset = max(buses) # to speed up the search
# while not is_valid(tstamp-offset):
#     tstamp += bus
#     # print(tstamp, end='\r')
# print(tstamp-offset)


# Using the Chinese remainder theorem is a lot more efficient...
# https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Existence_(direct_construction)
def eucl(r, u, v, rp, up, vp):
    if rp == 0:
        return (r, u, v)
    else:
        return eucl(rp, up, vp, r - (r//rp)*rp, u - (r//rp)*up, v - (r//rp)*vp)

def euclid(a, b):
    return eucl(a, 1, 0, b, 0, 1)

def solve(buses):
    product = 1
    for bus,_ in buses:
        product *= bus

    e = []
    for bus,offset in buses:
        _, u, v = euclid(bus, product//bus)
        e.append(-offset*v*product//bus)

    return sum(e)%product

print(solve(buses))
