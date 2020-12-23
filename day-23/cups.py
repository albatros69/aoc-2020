#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))
line = list(map(int, lines[0]))

class Cups():
    cups=None
    current=None
    limit=9

    def __init__(self, line, limit=9):
        self.cups = line + list(range(10, limit+1))
        self.current=0
        self.limit=limit

    def pickup(self):
        pos = (self.current+1)%self.limit
        pickup = self.cups[pos:pos+3]
        if len(pickup)<3:
            pickup+=self.cups[:3-len(pickup)]
        return pickup

    def insert(self, dest, chunk):
        for _ in range(3):
            try:
                self.cups.pop((self.current+1)%self.limit)
            except IndexError:
                self.cups.pop(0)
        pos = self.cups.index(dest)+1 # __index__
        for i,a in enumerate(chunk[::-1]):
            self.cups.insert(pos, a)
        if pos <= self.current:
            self.current += 3-max(3-(self.limit-1-self.current), 0)

    def move(self):
        dest = (self.cups[self.current]-2)%self.limit+1
        pickup = self.pickup()
        # print("pickup:", " ".join(map(str, pickup)))
        while dest in pickup:
            dest = (dest-2)%self.limit+1
        # print("destination:", dest)
        self.insert(dest, pickup)
        self.current = (self.current+1)%self.limit

    def __repr__(self):
        return "cups: " + " ".join(map(str, self.cups[:self.current])) + \
            " ({}) ".format(self.cups[self.current]) + \
            " ".join(map(str, self.cups[self.current+1:]))

    def result(self):
        index = self.cups.index(1)
        return ''.join(map(str, self.cups[index+1:])) + ''.join(map(str, self.cups[:index]))


# Part 1
game=Cups(list(map(int, line)), limit=9)
for i in range(1,101):
    # print(f"-- move {i} --")
    # print(game)
    game.move()
    # print()

print("-- final --"); print(game)
print(game.result())

# Part 2
class Cup():
    label=None
    next=None

    def __init__(self, val):
        self.label=val

    def __repr__(self):
        return "{}->{}".format(self.label, self.next.label if self.next else 'X' )


limit = 1000000
# limit = 9 # to test this solution for part 1

# # Takes too much time!
# game=Cups(list(map(int, lines[0])), limit=limit)
# for i in range(1,100000000):
#     print(f"-- move {i} --", end='\r')
#     game.move()

cups = { i: Cup(i) for i in range(1, limit+1) }
for i in range(1, limit):
    cups[i].next = cups[i+1]
cups[line[-1]].next = cups[len(line)+1]

curr=cups[line[0]]
for i in range(1, len(line)):
    cups[line[i-1]].next = cups[line[i]]
cups[limit].next = curr
# Uncomment below line if you want to use this solution for part 1 (and change the limit)
# cups[line[-1]].next = curr

for i in range(1, 10000001):
    # print(f'-- move {i} --', end='\r')

    pickup = [ curr.next, curr.next.next, curr.next.next.next ]
    labels = [ c.label for c in pickup ]
    curr.next = pickup[-1].next

    dest = (curr.label-2)%limit+1
    while dest in labels:
        dest = (dest-2)%limit+1

    pickup[-1].next = cups[dest].next
    cups[dest].next = pickup[0]

    curr=curr.next

print(cups[1].next.label * cups[1].next.next.label)

