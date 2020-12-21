#! /usr/bin/env python

import sys
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Tile():
    serial = None
    pixels = None
    dim = 0
    right = None
    left = None
    top = None
    bottom = None

    def __init__(self, serial, lines) -> None:
        self.serial = serial
        self.dim = len(lines)
        self.pixels = dict()
        for y,l in enumerate(lines):
            for x,pixel in enumerate(l):
                self.pixels[x,y] = pixel

    def borders(self):
        right, top, left, bottom = [], [], [], []
        for i in range(self.dim):
            right.append(self.pixels[self.dim-1,i])
            top.append(self.pixels[i,self.dim-1])
            left.append(self.pixels[0,i])
            bottom.append(self.pixels[i,0])
        return (right, top, left, bottom)

    def is_neigh(self, other):
        r,t,l,b = self.borders()
        ro,to,lo,bo = other.borders()

        if r==lo:
            self.right = other
            other.left = self
            return True
        elif t==bo:
            self.top = other
            other.bottom = self
            return True
        elif l==ro:
            self.left = other
            other.right = self
            return True
        elif b==to:
            self.bottom = other
            other.top = self
            return True

        return False

    def __repr__(self):
        return f"Tile {self.serial}:\n"+\
            "\n".join( (''.join([ self.pixels[x,y] for x in range(self.dim)]) for y in range(self.dim)) )

    def rotate(self):
        self.pixels = { (self.dim-1-y,x): self.pixels[x,y]
                    for x in range(self.dim) for y in range(self.dim) }

    def flip_h(self):
        self.pixels = { (x,y): self.pixels[x,self.dim-1-y]
                    for x in range(self.dim) for y in range(self.dim) }

    def flip_v(self):
        self.pixels = { (x,y): self.pixels[self.dim-1-x,y]
                    for x in range(self.dim) for y in range(self.dim) }

tiles = []
tmp = []; id = None
for l in lines:
    if l.startswith('Tile'):
        id = int(l[5:-1])
    elif l!='':
        tmp.append(l)
    else:
        tiles.append(Tile(id, tmp))
        tmp.clear()

if tmp:
    tiles.append(Tile(id, tmp))

neighbours = defaultdict(set)
transformations = ('flip_h', 'flip_v', 'flip_h', 'flip_v', 'rotate', ) * 4
tmp = tiles.copy()
grid = [ tmp.pop(0) ]
while tmp:
    j = tmp.pop(0)
    for i in grid:
        if len(neighbours[i.serial])==4:
            continue
        for action in transformations:
            if i.is_neigh(j):
                neighbours[i.serial].add(j.serial)
                neighbours[j.serial].add(i.serial)
                grid.append(j)
                break
            getattr(j, action)()
    if j not in grid: # no place found: we will retry later
        tmp.append(j)
    print(len(tmp), ' '*3, end='\r')

# Part 1
result = 1
for a in neighbours:
    if len(neighbours[a])==2:
        result *= a
print(result)

from math import sqrt

class Image(Tile): # to inherit all the transformations
    pixels = defaultdict(lambda: ' ')
    dim = None

    def __init__(self, dim):
        self.dim = dim

    def add_tile(self, x, y, tile: Tile):
        for i in range(1, tile.dim-1):
            for j in range(1, tile.dim-1):
                self.pixels[x+i-1,y+j-1]=tile.pixels[i,j]
        if tile.right is not None:# and x+tile.dim-2<self.dim:
            self.add_tile(x+tile.dim-2,y, tile.right)
        if tile.left is None and tile.top is not None:# and y+tile.dim-2<self.dim:
            self.add_tile(x,y+tile.dim-2, tile.top)

    # To test with the borders and especially with test2 for a visual check
    # def add_tile(self, x, y, tile: Tile):
    #     for i in range(0, tile.dim):
    #         for j in range(0, tile.dim):
    #             self.pixels[x+i,y+j]=tile.pixels[i,j]
    #     if tile.right is not None:# and x+tile.dim<self.dim:
    #         self.add_tile(x+tile.dim,y, tile.right)
    #     if tile.left is None and tile.top is not None:# and y+tile.dim<self.dim:
    #         self.add_tile(x,y+tile.dim, tile.top)

    def __repr__(self):
        return f"Image:\n"+\
            "\n".join( (''.join([ self.pixels[x,y] for x in range(self.dim)]) for y in range(self.dim)) )

    def match_pattern(self, x,y, pattern):
        if (x+pattern.dim[0])>=self.dim or (y+pattern.dim[1])>=self.dim:
            return False

        for i in range(pattern.dim[0]):
            for j in range(pattern.dim[1]):
                if not (pattern.pixels[i,j]==' ' or
                        pattern.pixels[i,j]==self.pixels[x+i,y+j]):
                    return False
        return True

    def apply_pattern(self, x,y, pattern):
        for i in range(pattern.dim[0]):
            for j in range(pattern.dim[1]):
                if pattern.pixels[i,j]=='#':
                    self.pixels[x+i,y+j]='O'


image = Image(int(sqrt(len(tiles))*(tiles[0].dim-2)))
for tile in tiles:
    if tile.bottom is None and tile.left is None:
        # bottom-left corner
        image.add_tile(0, 0, tile)
        break

class Pattern():
    pixels = None
    dim = None

    def __init__(self, lines) -> None:
        self.pixels = dict()
        for y,l in enumerate(lines):
            self.dim = (len(l), len(lines))
            for x,pixel in enumerate(l):
                self.pixels[x,y] = pixel

    def __repr__(self):
        return "Pattern:\n"+\
            "\n".join( (''.join([ self.pixels[x,y] for x in range(self.dim[0])]) for y in range(self.dim[1])) )

monster = Pattern([
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "])


for action in transformations:
    result = False
    for x in range(image.dim):
        for y in range(image.dim):
            if image.match_pattern(x,y, monster):
                result=True
                image.apply_pattern(x,y, monster)
    if result:
        break
    else:
        getattr(image, action)()

print(image)
print(sum( image.pixels[x,y]=='#' for x in range(image.dim) for y in range(image.dim) ))