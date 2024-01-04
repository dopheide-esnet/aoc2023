#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

class Card:
    def __init__(self,num,winners,mine):
        self.num = num
        self.winners = winners
        self.mine = mine
        self.wins = 0
        self.score = 0
        self.copies = 1
    def print(self):
        print(f"Card {self.num}: {self.wins}: {self.score}")

def BuildCards(lines):
    cards = dict()
    for line in lines:
        (c,d) = line.split(":")
        m = re.search(r'Card\s+(\d+)$',c)
        if(m):
            cn = m.group(1)
        (w,m) = d.split("|")
        winners = w.split(" ")
        mine = m.split(" ")
        winners = [int(i) for i in winners if i]
        mine = [int(i) for i in mine if i]
        cards[int(cn)] = Card(cn,winners,mine)
    return cards

def ProcessCards(cards):
    for c in cards:
        for num in cards[c].mine:
            if num in cards[c].winners:
                cards[c].wins += 1
        if(cards[c].wins > 0):
            cards[c].score = 2 ** (cards[c].wins - 1)

def PrintCards(cards):
    for c in cards:
        cards[c].print()

if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    cards = BuildCards(lines)
    ProcessCards(cards)

#    PrintCards(cards)
    total = 0
    total_cards = 0
    for c in cards:
        total += cards[c].score
        total_cards += cards[c].copies
        for i in range(1,cards[c].wins+1):
            cards[c+i].copies += cards[c].copies  # right?   

    print("Part 1:",total)
    print("Part 2:",total_cards)