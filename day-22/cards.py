#! /usr/bin/env python

import sys
from copy import deepcopy

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Player():
    number=0
    deck=None

    def __init__(self, nb, lines) -> None:
        self.number=nb
        self.deck=[]
        for l in lines:
            self.deck.append(int(l))

    def play(self):
        return self.deck.pop(0)

    def win(self, a, b):
        # print(f'Player {self.number} wins!')
        self.deck.extend([a,b])

    def __repr__(self):
        return f"Player {self.number}'s deck: " + \
            " ".join(map(str, self.deck))

    def has_cards(self):
        return len(self.deck)>0

    def score(self):
        return sum( (i+1)*c for i,c in enumerate(self.deck[::-1]) )

players = []
tmp = []; id = None
for l in lines:
    if l.startswith('Player'):
        id = int(l[7:-1])
    elif l!='':
        tmp.append(l)
    else:
        players.append(Player(id, tmp))
        tmp.clear()

if tmp:
    players.append(Player(id, tmp))

class Game():
    players = []
    round=0
    memory=None

    def can_continue(self):
        return all(p.has_cards() for p in self.players)

    def play_round_part1(self):
        self.round+=1
        # print('---', f"Round {self.round}", '---')
        # for p in self.players:
        #     print(p)
        p1, p2 = [ p.play() for p in self.players ]
        # print(f"Player 1 plays: {p1}")
        # print(f"Player 2 plays: {p2}")
        if p1>p2:
            self.players[0].win(p1,p2)
        else:
            self.players[1].win(p2,p1)

    def run_part1(self):
        while self.can_continue():
            self.play_round_part1()
        print("== Post-game results ==")
        for p in self.players:
            print(p, "-->", p.score())

    def play_round_part2(self):
        self.round+=1

        # print('---', f"Round {self.round}", '---')
        # for p in self.players:
        #     print(p)

        if (tuple(self.players[0].deck), tuple(self.players[1].deck)) in self.memory:
            self.players[1].deck=[] # Player 1 wins instantly
            return
        else:
            self.memory.add((tuple(self.players[0].deck), tuple(self.players[1].deck)))

        p1, p2 = [ p.play() for p in self.players ]
        # print(f"Player 1 plays: {p1}")
        # print(f"Player 2 plays: {p2}")
        if p1 <= len(self.players[0].deck) and p2 <= len(self.players[1].deck):
            tmp = self.spawn(p1, p2)
            tmp.run_part2()
            if len(tmp.players[0].deck)>0: # P1 winned sub-game
                self.players[0].win(p1,p2)
            else:
                self.players[1].win(p2,p1)
        elif p1>p2:
            self.players[0].win(p1,p2)
        else:
            self.players[1].win(p2,p1)

    def run_part2(self):
        while self.can_continue():
            self.play_round_part2()
        # print("== Post-game results ==")
        # for p in self.players:
        #     print(p, "-->", p.score())

    def spawn(self, a,b):
        tmp = Game()
        tmp.players = deepcopy(self.players)
        tmp.memory = set() #self.memory
        tmp.players[0].deck = tmp.players[0].deck[:a]
        tmp.players[1].deck = tmp.players[1].deck[:b]
        return tmp

# Part 1
game=Game()
game.players=deepcopy(players)
game.run_part1()

# Part 2
game=Game()
game.players=deepcopy(players)
game.memory=set()
game.run_part2()
print("== Post-game results ==")
for p in game.players:
    print(p, "-->", p.score())
