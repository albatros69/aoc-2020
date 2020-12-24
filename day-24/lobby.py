#! /usr/bin/env python

import sys
from collections import defaultdict
from copy import copy, deepcopy

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def readline(line):
    cursor=0
    result=[]
    while cursor<len(line):
        if line[cursor:cursor+2] in ('se', 'sw', 'ne', 'nw'):
            result.append(line[cursor:cursor+2])
            cursor+=2
        else:
            result.append(line[cursor])
            cursor+=1
    return result


flipped=[]
for l in lines:
    flipped.append(readline(l))


class Tile():
    x=0
    y=0
    color='w'

    def __init__(self, x=0, y=0) -> None:
        self.x=x
        self.y=y

    def __repr__(self):
        return "({0.x},{0.y})={0.color}".format(self)

    def move(self, dir):
        if dir=='e':
            self.x+=1
        elif dir=='w':
            self.x-=1
        elif dir=='ne':
            self.x+=self.y%2
            self.y+=1
        elif dir=='nw':
            self.y+=1
            self.x-=self.y%2
        elif dir=='se':
            self.x+=self.y%2
            self.y-=1
        elif dir=='sw':
            self.y-=1
            self.x-=self.y%2
        else:
            raise NotImplemented

    def flip(self):
        if self.color=='w':
            self.color='b'
        else:
            self.color='w'

    def neighbours(self):
        return ((self.x+1, self.y), (self.x-1, self.y), # E, W
            (self.x+self.y%2, self.y+1), (self.x-(self.y+1)%2, self.y+1), # NE, NW
            (self.x+self.y%2, self.y-1), (self.x-(self.y-1)%2, self.y-1), # SE, SW
        )

floor = defaultdict(lambda: Tile())

for moves in flipped:
    tile = Tile()
    for m in moves:
        tile.move(m)
    tile.color = floor[tile.x,tile.y].color
    tile.flip()
    floor[tile.x,tile.y] = tile
    for n in tile.neighbours():
        if n not in floor:
            floor[n] = Tile(*n)

print('-- Part 1 --')
print(sum(floor[t].color=='b' for t in floor))

def step(floor):
    new_floor = deepcopy(floor)
    for tile in floor:
        nb_b=0
        for n in floor[tile].neighbours():
            if n in floor:
                nb_b+= int(floor[n].color=='b')
            else:
                # to check them the day after
                new_floor[n]=Tile(*n)

        if floor[tile].color=='b' and (nb_b==0 or nb_b>2):
            new_floor[tile].flip()
        elif floor[tile].color=='w' and nb_b==2:
            new_floor[tile].flip()
        else:
            pass
    return new_floor

print('-- Part 2 --')
for day in range(1, 101):
    floor=step(floor)
    if day<=10 or day%10==0:
        print("Day {}: {}".format(day, sum(floor[t].color=='b' for t in floor)))
