#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

hand_types = {'fivekind': 7, 'fourkind': 6, 'fullhouse': 5, 'threekind': 4,
              'twopair': 3, 'onepair': 2, 'high': 1}
hand_labels = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}  # else label = int
joker_hand_labels = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10}  # else label = int

def TestWorks():
    return True

class Hand:
    def __init__(self,hand,bid):
        self.hand = hand
        self.bid = bid
        self.kinds = list() # the labels if we have three, four, five-of-a-kind or pairs.
        self.type = None    # we'll make this an integer for faster sorting
    def __lt__(self,other):
        # based on type
        if(self.type != other.type):
            return self.type < other.type
        else:
        # or high card
            for i in range(len(self.hand)):
                if(self.hand[i] != other.hand[i]):
                    return self.hand[i] < other.hand[i]
    def print(self):
        print(self.hand,self.bid,self.type,self.kinds)

def BuildHands(lines):
    hand_re = re.compile(r'(\w)(\w)(\w)(\w)(\w)\s(\d+)$')
    hands = list()
    for line in lines:
        m = hand_re.search(line)
        hand = list()
        if(m):
            for i in range(1,6):
                card = m.group(i)
                if card in hand_labels:
                    val = hand_labels[card]
                else:
                    val = int(card)
                hand.append(val)
            bid = int(m.group(6))
            hands.append(Hand(hand,bid))
    return hands

def BuildJokerHands(lines):
    hand_re = re.compile(r'(\w)(\w)(\w)(\w)(\w)\s(\d+)$')
    hands = list()
    for line in lines:
        m = hand_re.search(line)
        hand = list()
        if(m):
            for i in range(1,6):
                card = m.group(i)
                if card in joker_hand_labels:
                    val = joker_hand_labels[card]
                else:
                    val = int(card)
                hand.append(val)
            bid = int(m.group(6))
            hands.append(Hand(hand,bid))
    return hands

def GetTypes(hands):
    for h in hands:
        shand = h.hand.copy()
        shand.sort(reverse=True)

        # there's gotta be a better way, but we only have to do this once.
        if(shand[0] == shand[1] and shand[1] == shand[2] and shand[2] == shand[3] and shand[3] == shand[4]):
            type = hand_types['fivekind']
            h.kinds.append(shand[0])
        elif((shand[0] == shand[1] and shand[1] == shand[2] and shand[2] == shand[3]) or
             (shand[1] == shand[2] and shand[2] == shand[3] and shand[3] == shand[4])):
            type = hand_types['fourkind']
            h.kinds.append(shand[1])
        elif(shand[0] == shand[1] and shand[1] == shand[2]):
            h.kinds.append(shand[0])
            if(shand[3] == shand[4]):
                type = hand_types['fullhouse']
                h.kinds.append(shand[3])
            else:
                type = hand_types['threekind']
        elif(shand[2] == shand[3] and shand[3] == shand[4]):
            h.kinds.append(shand[2])
            if(shand[0] == shand[1]):
                type = hand_types['fullhouse']
                h.kinds.append(shand[0])
            else:
                type = hand_types['threekind']
        elif(shand[1] == shand[2] and shand[2] == shand[3]):
            h.kinds.append(shand[2])
            type = hand_types['threekind']
        elif(shand[0] == shand[1] and (shand[2] == shand[3] or shand[3] == shand[4])):
            h.kinds.append(shand[0])
            h.kinds.append(shand[3])
            type = hand_types['twopair']
        elif(shand[1] == shand[2] and shand[3] == shand[4]):
            type = hand_types['twopair']
            h.kinds.append(shand[1])
            h.kinds.append(shand[3])
        elif(shand[0] == shand[1] or shand[1] == shand[2] or shand[2] == shand[3] or shand[3] == shand[4]):
            type = hand_types['onepair']
            if(shand[0] == shand[1]):
                h.kinds.append(shand[0])
            elif(shand[1] == shand[2]):
                h.kinds.append(shand[1])
            elif(shand[2] == shand[3]):
                h.kinds.append(shand[2])
            elif(shand[3] == shand[4]):
                h.kinds.append(shand[3])
        else:
            type = hand_types['high']
        
        h.type = type
        # Joker adjustments?
        if(1 in shand):
            # how many?  Remember this is sorted and J's are '1'
            jokers = 1
            if(shand[3] == 1):
                jokers += 1
                if(shand[2] == 1):
                    jokers += 1
                    if(shand[1] == 1):
                        jokers += 1
                        h.type = hand_types['fivekind']
                        # no other way it could be.
            if(jokers == 3):
                if(h.type == 5):  # we had a full house before
                    h.type = hand_types['fivekind']
                else:  # otherwise just a three of a kind of jokers which gives us four
                    h.type = hand_types['fourkind']
            elif(jokers == 2):
                if(h.type == 5): # again a full house before
                    h.type = hand_types['fivekind']
                elif(h.type == 3):  # we had two pair
                    h.type = hand_types['fourkind']
                elif(h.type == 2):  # we have just this pair of jokers
                    h.type = hand_types['threekind']
                else:
                    print("not possible")
                    exit(1)
            elif(jokers == 1):
                if(h.type == 6):
                    h.type = hand_types['fivekind']
                elif(h.type == 4):
                    h.type = hand_types['fourkind']
                elif(h.type == 3):
                    h.type = hand_types['fullhouse']
                elif(h.type == 2):
                    h.type = hand_types['threekind']
                else:
                    h.type = hand_types['onepair']

if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    hands = BuildHands(lines)
    hands = BuildJokerHands(lines)
    GetTypes(hands)

    hands.sort()

#    for hand in hands:
#        hand.print()

    total = 0
    for i in range(len(hands)):
        total += hands[i].bid * (i + 1)
    print("Total:",total)




