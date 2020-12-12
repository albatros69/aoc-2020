#! /usr/bin/env python

import sys
from collections import namedtuple

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

Position=namedtuple('Position', ('x', 'y'))

class ShipPart1():
    position = Position(0, 0)
    directions = { 'E': Position(1,0), 'N': Position(0,1), 'W': Position(-1,0), 'S': Position(0,-1) }
    direction = Position(1,0)

    def move(self, direction, val):
        self.position = Position(
            self.position.x + val*direction.x, self.position.y + val*direction.y
        )

    def rotate_90(self, direction):
        if direction == 'L':
            self.direction = Position(-self.direction.y, self.direction.x)
        else:
            self.direction = Position(self.direction.y, -self.direction.x)

    def rotate(self, direction, angle):
        for _ in range(angle//90):
            self.rotate_90(direction)

    def apply_instruction(self, cmd, val):
        if cmd=='F':
            self.move(self.direction, val)
        elif cmd in self.directions.keys():
            self.move(self.directions[cmd], val)
        elif cmd in ('R', 'L'):
            self.rotate(cmd, val)

    def print(self):
        print("Pos: {0.x}, {0.y} toward {1.x}, {1.y}".format(self.position, self.direction))

    def distance(self):
        return sum(map(abs, self.position))


# Part 1
ship = ShipPart1()
# print('Start: ', end='') ; ship.print()

for l in lines:
    # print(l, end=' --> ')
    ship.apply_instruction(l[0], int(l[1:]))
    # ship.print()

print(ship.distance())


class ShipPart2(ShipPart1):
    direction = Position(10,1) # waypoint

    def move_waypoint(self, direction, val):
        self.direction = Position(
            self.direction.x + val*direction.x, self.direction.y + val*direction.y
        )

    def apply_instruction(self, cmd, val):
        if cmd=='F':
            self.move(self.direction, val)
        elif cmd in self.directions.keys():
            self.move_waypoint(self.directions[cmd], val)
        elif cmd in ('R', 'L'):
            self.rotate(cmd, val)


# Part 2
ship = ShipPart2()
# print('Start: ', end='') ; ship.print()

for l in lines:
    # print(l, end=' --> ')
    ship.apply_instruction(l[0], int(l[1:]))
    # ship.print()

print(ship.distance())
