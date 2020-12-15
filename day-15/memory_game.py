#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Game():
    def __init__(self, starting_numbers):
        self.memory = { n: i+1 for i,n in enumerate(starting_numbers) }
        self.current_turn = len(starting_numbers)+1
        self.last_number = starting_numbers[-1]
        self.next_number = None

    def next_turn(self):
        if self.last_number not in self.memory:
            # First time seen
            self.next_number = 0
        else:
            self.next_number = self.current_turn - self.memory[self.last_number] - 1

        self.memory[self.last_number] = self.current_turn-1
        self.current_turn += 1
        self.last_number = self.next_number

for l in lines:
    # Part 1
    end = 2020
    # Part 2
    # end = 30000000
    game = Game([int(i) for i in l.split(',') ])
    for _ in range(len(l.split(',')), end):
        game.next_turn()

    print(game.last_number)
