#!/usr/bin/env python3

import re
import math

testcase = False
if testcase:
    file = "test2.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

class Map:
    def __init__(self,left,right):
        self.left = left
        self.right = right

def BuildTable(lines):
    table = dict()
    line_re = re.compile(r'(\w\w\w) = \((\w\w\w), (\w\w\w)\)')
    for line in lines:
        m = line_re.search(line)
        if(m):
            key = m.group(1)
            left = m.group(2)
            right = m.group(3)
            table[key] = Map(left,right)

    return table

def FindSteps(ins,table):
    loc = 'AAA'
    steps = 0
    i = 0
    while(loc != 'ZZZ'):
        if(ins[i] == 'R'):
            loc = table[loc].right
        else:
            loc = table[loc].left
        i+=1
        if(i == len(ins)):
            i = 0
        steps += 1
    return steps

def FindZSteps(i,loc,ins,table):
    steps = 0
    start = False
    while(loc[-1] != 'Z' or start==False):
        start = True
        if(ins[i] == 'R'):
            loc = table[loc].right
        else:
            loc = table[loc].left
        i+=1
        if(i == len(ins)):
            i = 0
        steps += 1
#    print("Found Z at",loc,i,steps)
    return (steps,i,loc)

def FindLoop(loc,ins,table):
    i = 0
    (start_steps,i,new_loc) = FindZSteps(i,loc,ins,table)

    # now we're at a Z
    # how many steps to get back to a Z?
    # Man I hope there aren't multiple Z's inside a loop.
    (steps,i,new_loc) = FindZSteps(i,new_loc,ins,table)

    return (start_steps,steps)

def CheckDst(dst):
    goal = dst[0]
    for i in range(1,len(dst)):
        if(dst[i] != goal):
            return False
    return True

if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    instructions = list(lines.pop(0))
    lines.pop(0)

    table = BuildTable(lines)
#    steps = FindSteps(instructions,table)
#    print("Part 1:",steps)

    # Part 2, gee thanks
    starts = list()
    for loc in table:
        if(loc[-1] == 'A'):
            starts.append(loc)

#    for t in table:
#        print(t,table[t].left,table[t].right)

    steps_list = list()
    for loc in starts:
        steps_list.append(FindLoop(loc,instructions,table))
    print("Part 2:",steps_list)


    # Math is hard
    dst = list()
    for i in range(len(steps_list)):
        (s,z) = steps_list[i]
        dst.append(s)
    print(dst)

#    while(not CheckDst(dst)):
        # this is so dumb, just add steps to the minimum until they're all equal
#        my_min = min(dst)
#        i = dst.index(my_min)
#        (s,z) = steps_list[i]
#        dst[i] += z

#    print("Part 2:",dst[0])
    mult = list()
    for (s,i) in steps_list:
        mult.append(s)

    print(math.lcm(*mult))



