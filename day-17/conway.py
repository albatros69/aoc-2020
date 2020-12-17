#! /usr/bin/env python

import sys
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def constant_factory(value):
    return lambda: value

class Grid3():

    def __init__(self, lines):
        self.grid = defaultdict(constant_factory('.'))
        self.tmp_grid = defaultdict(constant_factory('.'))
        self.cells = set()

        for y,l in enumerate(lines):
            for x,c in enumerate(l):
                self.grid[x,y,0] = c
                self.cells.update(self.neighbours(x,y,0))

    def neighbours(self, x, y, z):
        return set( (x+a,y+b,z+c)
            for a in (-1,0,1) for b in (-1,0,1) for c in (-1,0,1)
            if (a,b,c)!=(0,0,0) )

    def change_status(self, x, y, z):
        active_neigh = 0
        new_cells = []
        for pt in self.neighbours(x,y,z):
            new_cells.append(pt) # to be considered in the next turn
            if self.grid[pt] == '#':
                active_neigh += 1

        if self.grid[x,y,z] == '#' and (active_neigh<2 or active_neigh>3):
            self.tmp_grid[x,y,z] = '.'
        elif self.grid[x,y,z] == '.' and active_neigh == 3:
            self.tmp_grid[x,y,z] = '#'
        else:
            self.tmp_grid[x,y,z] = self.grid[x,y,z]

        return new_cells
        
    def cycle(self):
        new_cells = []
        self.tmp_grid.clear()
        for cell in self.cells:
            new_cells.extend(self.change_status(*cell))
        self.cells.update(new_cells)
        self.grid = self.tmp_grid.copy()

    @property
    def active_cells(self):
        return sum(self.grid[cell]=='#' for cell in self.grid)
    

# Part 1
grid = Grid3(lines)
for _ in range(6):
    grid.cycle()
print(grid.active_cells)

# Part 2
class Grid4():

    def __init__(self, lines):
        self.grid = defaultdict(constant_factory('.'))
        self.tmp_grid = defaultdict(constant_factory('.'))
        self.cells = set()

        for y,l in enumerate(lines):
            for x,c in enumerate(l):
                self.grid[x,y,0,0] = c
                self.cells.update(self.neighbours(x,y,0,0))

    def neighbours(self, x, y, z, w):
        return set( (x+a,y+b,z+c,w+d)
            for a in (-1,0,1) for b in (-1,0,1) for c in (-1,0,1) for d in (-1,0,1)
            if (a,b,c,d)!=(0,0,0,0) )

    def change_status(self, x, y, z, w):
        active_neigh = 0
        new_cells = []
        for pt in self.neighbours(x,y,z,w):
            new_cells.append(pt) # to be considered in the next turn
            if self.grid[pt] == '#':
                active_neigh += 1

        if self.grid[x,y,z,w] == '#' and (active_neigh<2 or active_neigh>3):
            self.tmp_grid[x,y,z,w] = '.'
        elif self.grid[x,y,z,w] == '.' and active_neigh == 3:
            self.tmp_grid[x,y,z,w] = '#'
        else:
            self.tmp_grid[x,y,z,w] = self.grid[x,y,z,w]

        return new_cells
        
    def cycle(self):
        new_cells = []
        self.tmp_grid.clear()
        for cell in self.cells:
            new_cells.extend(self.change_status(*cell))
        self.cells.update(new_cells)
        self.grid = self.tmp_grid.copy()

    @property
    def active_cells(self):
        return sum(self.grid[cell]=='#' for cell in self.grid)
    
grid = Grid4(lines)
for _ in range(6):
    grid.cycle()
print(grid.active_cells)
