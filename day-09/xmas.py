#! /usr/bin/env python

import collections
import sys
from itertools import combinations

lines = []
for line in sys.stdin:
    lines.append(int(line.rstrip('\n')))


class Decipher():
    
    def __init__(self, preamble_length):
        self.preamble_length = preamble_length
        self.cursor = 0
        self.data = []
    
    def read_next(self, value):
        if len(self.data) < self.preamble_length: # Still reading the preamble
            self.data.append(value)
            return True
        else:
            assert(self.cursor + self.preamble_length == len(self.data)) 
            if self.is_valid(value):
                self.cursor += 1 # We move the head of the sliding window
                self.data.append(value) # and add the new valid value at the end
                return True
            else:
                return False
    
    def is_valid(self, value):
        for (a,b) in combinations(self.data[self.cursor:], 2):
            if a+b == value:
                return True

        return False
    

# Test
# test = Decipher(5)
# for l in lines:
# 	if not test.read_next(int(l)):
# 		print(l)
# 		break

# Part 1
input = Decipher(25)
error = None
for l in lines:
    if not input.read_next(l):
        error = l
        print(error)
        break

# Part 2
# Looking for a subset of contiguous values whose sum is egal to the invalid value
for start in range(0, input.cursor):
    for end in range(1, input.cursor+1):
        if sum(input.data[start:end]) == error:
            print(min(input.data[start:end])+max(input.data[start:end]))
            break
