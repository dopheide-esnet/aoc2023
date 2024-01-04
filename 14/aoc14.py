#!/usr/bin/env python3

import copy

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def BuildPlatform(lines):
    plat = list()
    for line in lines:
        plat.append(list(line))
    return plat

def RollNorth(plat):
    for y in range(1,len(plat)):  # first row can't move up
        for x in range(len(plat[0])):
            if(plat[y][x] == 'O'):
                move = False
                for j in reversed(range(y)):
#                    print("j",j)
                    if(plat[j][x] == '.'):   # can move up
                        move = True
                    else:
                        if(move):
                            j += 1  # cause we're reversed
                        break
                if(move):
                    plat[y][x] = '.'
                    plat[j][x] = 'O' 

def RollWest(plat):
    for y in range(len(plat)):  
        for x in range(1,len(plat[0])): # first row can't move west
            if(plat[y][x] == 'O'):
                move = False
                for j in reversed(range(x)):
#                    print("j",j)
                    if(plat[y][j] == '.'):   # can move west
                        move = True
                    else:
                        if(move):
                            j += 1  # cause we're reversed
                        break
                if(move):
                    plat[y][x] = '.'
                    plat[y][j] = 'O' 

# gotta start from the bottom.
def RollSouth(plat):
    x_len = len(plat[0])
    y_len = len(plat)
    for y in reversed(range(len(plat)-1)):  # last row can't move down
        for x in range(x_len):
            if(plat[y][x] == 'O'):
                move = False
                for j in range(y+1,y_len):
#                    print("j",j)
                    if(plat[j][x] == '.'):   # can move down
                        move = True
                    else:
                        if(move):
                            j -= 1
                        break
                if(move):
                    plat[y][x] = '.'
                    plat[j][x] = 'O' 


def RollEast(plat):
    x_len = len(plat[0])
    y_len = len(plat)
    for y in range(y_len):  # last row can't move east
        for x in reversed(range(len(plat)-1)):
            if(plat[y][x] == 'O'):
                move = False
                for j in range(x+1,x_len):
#                    print("j",j)
                    if(plat[y][j] == '.'):   # can move up
                        move = True
                    else:
                        if(move):
                            j -= 1
                        break
                if(move):
                    plat[y][x] = '.'
                    plat[y][j] = 'O' 


def GetLoad(plat):
    weight = 0
    platlen = len(plat)
    for y in range(len(plat)):
        for x in range(len(plat[0])):
            if(plat[y][x] == 'O'):
                weight += platlen - y
    return weight

def Compare(plat,all_states):

    # can probably improve efficieny of this comparison
    for a in range(len(all_states)):
        match = True
        for y in range(len(plat)):
            for x in range(len(plat[0])):
                if(plat[y][x] != all_states[a][y][x]):
                    match = False
                    break
            if(not match):
                break
        if(match):
            return (match,a)

    return (False,0)

if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    plat = BuildPlatform(lines)

#    for p in plat:
#        print("".join(p))

#    RollNorth(plat)
#    for p in plat:
#        print("".join(p))
#    weight = GetLoad(plat)
#    print("Part1 Weight",weight)


    cycles = 1000000000
    all_states = list()
    first = list()
    for c in range(cycles):
        RollNorth(plat)
        RollWest(plat)
        RollSouth(plat)
        RollEast(plat)
        if(len(all_states) > 0):
            if(len(first) == 0):
                (match,a) = Compare(plat,all_states)
                if not match:
                    all_states.append(copy.deepcopy(plat))
                else:
                    print("Match found at cycle c with node a",c,a)
                    # first match isn't necessarily the loop?
                    # we need to know when we see it again
                    first.append(copy.deepcopy(plat))
                    break # skip second
            else:
                (match,a) = Compare(plat,first)
                if not match:
                    all_states.append(copy.deepcopy(plat))
                else:
                    print("Second match found at cycle c with node a",c,a)
                    # first match isn't necessarily the loop?
                    # we need to know when we see it again
                    # nope, it's still the same loop size
                    break
             
        else:
            all_states.append(copy.deepcopy(plat))

    loop = c - a
    print("Loop:",loop)

    # loop starts at index 'a'
    # so the first a-1 things in the index we don't need
    # as well as the first a-1 cycles.
    cycles = cycles - (a - 1)
    remainder = cycles % loop
    print("rem:",remainder)   # spot in the loop (but not in our full index)
    index = (a-1)+remainder-1
    print("index",index)


    # we don't use the first 'a' states in our set
    # example: we only care about states 2-8

    # not 84332
    weight = GetLoad(all_states[index])

#    for p in plat:
#        print("".join(p))
    print("Part2 Weight",weight)

#  Part 2, we're going to have to look for repeat cycles
