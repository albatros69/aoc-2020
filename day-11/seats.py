#! /usr/bin/env python

import sys
from collections import namedtuple

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

room = [ list(l) for l in lines ]

Size=namedtuple('Size', ('w', 'h'))

class Room():
    seats = []
    size = Size(0, 0)
    empty='L'
    occupied='#'

    def __init__(self, input):
        self.seats = [ list(l) for l in input ]
        self.size = Size(w=len(self.seats[0]), h=len(self.seats))

    def occupied_neigh(self, row, col):
        """ Counting all the occupied neighbour seats """
        neighbours=0
        for y in range(row-1, row+2):
            for x in range(col-1,col+2):
                if 0 <= y < self.size.h and 0 <= x < self.size.w and (y,x) != (row, col):
                    neighbours += int(self.seats[y][x]==self.occupied)

        return neighbours

    def change_seat_part1(self, row, col):
        nb_occupied = self.occupied_neigh(row,col)

        if self.seats[row][col]==self.empty and nb_occupied == 0:
            return self.occupied
        elif self.seats[row][col]==self.occupied and nb_occupied >= 4:
            return self.empty
        else:
            return self.seats[row][col]

    def visible_occupied(self, row, col):
        """ Counting the occupied seats visible in every directions """
        directions=((y,x) for y in (-1, 0 , 1) for x in (-1, 0, 1) if (y,x) != (0,0))
        nb_visible = 0

        for d in directions: # for each direction
            y,x = (row+d[0], col+d[1])
            while (0<=y<self.size.h) and (0<=x<self.size.w): # we're still in the room
                if self.seats[y][x]==self.occupied: # seat occupied
                    nb_visible += 1
                    break # all the remaining seats are invisible
                elif self.seats[y][x]==self.empty: # seat empty
                    break # all the remaining seats are invisible
                y,x = (y+d[0], x+d[1]) # otherwise, we continue in this direction

        return nb_visible

    def change_seat_part2(self, row, col):
        nb_occupied = self.visible_occupied(row,col)

        if self.seats[row][col]==self.empty and nb_occupied == 0:
            return self.occupied
        elif self.seats[row][col]==self.occupied and nb_occupied >= 5:
            return self.empty
        else:
            return self.seats[row][col]

    def change_room(self, part='part1'):
        new_seats = [ [ getattr(self, 'change_seat_'+part)(y, x) for x in range(self.size.w) ]
                        for y in range(self.size.h) ]
        self.seats = new_seats

    @property
    def nb_occupied(self):
        """ Count the number of occupied seats in the whole room """
        return sum(( self.seats[y][x]==self.occupied for y in range(self.size.h) for x in range(self.size.w) ))

    def print(self):
        """ To allow for step-by-step verifications """
        for y in range(self.size.h):
            print(''.join(self.seats[y]))


# Part 1
room = Room(lines)

# room.print(); print('-'*8)
# room.change_room('part2')
# room.print(); print('-'*8)
# room.change_room('part2')
# room.print(); print('-'*8)
# room.change_room('part2')
# room.print(); print('-'*8)

while True:
    nb_occupied = room.nb_occupied
    room.change_room('part1')
    if room.nb_occupied == nb_occupied:
        break

print(nb_occupied)

# Part 2
room = Room(lines)

# room.print(); print('-'*8)
# room.change_room('part2')
# room.print(); print('-'*8)
# room.change_room('part2')
# room.print(); print('-'*8)
# room.change_room('part2')
# room.print(); print('-'*8)

while True:
    nb_occupied = room.nb_occupied
    room.change_room('part2')
    if room.nb_occupied == nb_occupied:
        break

print(nb_occupied)
