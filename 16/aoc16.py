#!/usr/bin/env python3

import sys
sys.setrecursionlimit(3000)

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

class Location:
    def __init__(self,mirror):
        self.mirror = mirror
        self.beams = list()  # > < ^ v  Does this team exist here already?

def PrintMap(map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            print(map[y][x].mirror,end='')
        print("")

def PrintEnergized(map):
    energized = 0
    for y in range(len(map)):
        for x in range(len(map[0])):
            if(len(map[y][x].beams) > 1 ):
                print(len(map[y][x].beams),end='')
                energized += 1
            elif(len(map[y][x].beams) == 1):
                print(map[y][x].beams[0],end='')
                energized += 1
            else:
                print(".",end='')
        print("")
    return energized

def CountEnergized(map):
    energized = 0
    for y in range(len(map)):
        for x in range(len(map[0])):
            if(len(map[y][x].beams) > 0):
                energized+=1
    return energized

def BuildMap(lines):
    map = list()
    for line in lines:
        row = list()
        for x in list(line):
            row.append(Location(x))
        map.append(row)
    return(map)

def GetNewLoc(facing,loc,my,mx):
    (y,x) = loc
    if(facing == ">" and x < mx - 1):
        return ((y,x+1),True)
    elif(facing == "<" and x > 0):
        return ((y,x-1),True)
    elif(facing == "^" and y > 0):
        return ((y-1,x),True)
    elif(facing == "v" and y < my - 1):
        return ((y+1,x),True)
    return ((0,0),False)


def ProcessBeam(facing,loc,map,d):
    d += 1
#    print("d",d)
    (y,x) = loc
    my = len(map)
    mx = len(map[0])
    # a beam keeps going until it enters a square
    # with a beam headed the same direction
    if(facing in map[y][x].beams):
        return
    else:
        map[y][x].beams.append(facing)
    
    if(map[y][x].mirror == "."):
        (new_loc,valid) = GetNewLoc(facing,loc,my,mx)
        if(valid):
            ProcessBeam(facing,new_loc,map,d)
        return
    elif(map[y][x].mirror == "|"):
        # split beam if facing == ^ or v
        # bypass otherwise
        if(facing == "v" or facing == "^"):
            (new_loc,valid) = GetNewLoc(facing,loc,my,mx)
            if(valid):
                ProcessBeam(facing,new_loc,map,d)
            return
        else:
            new_facing = "^"
            (new_loc,valid) = GetNewLoc(new_facing,loc,my,mx)
            if(valid):
                ProcessBeam(new_facing,new_loc,map,d)
            new_facing = "v"
            (new_loc,valid) = GetNewLoc(new_facing,loc,my,mx)
            if(valid):
                ProcessBeam(new_facing,new_loc,map,d)
            return       
    elif(map[y][x].mirror == "-"):
        if(facing == ">" or facing == "<"):
            (new_loc,valid) = GetNewLoc(facing,loc,my,mx)
            if(valid):
                ProcessBeam(facing,new_loc,map,d)
            return
        else:
            new_facing = "<"
            (new_loc,valid) = GetNewLoc(new_facing,loc,my,mx)
            if(valid):
                ProcessBeam(new_facing,new_loc,map,d)
            new_facing = ">"
            (new_loc,valid) = GetNewLoc(new_facing,loc,my,mx)
            if(valid):
                ProcessBeam(new_facing,new_loc,map,d)
            return  
    elif((map[y][x].mirror == "/" and (facing == "^")) or
         (map[y][x].mirror == "\\" and (facing == "v"))):
        new_facing = ">"
        (new_loc,valid) = GetNewLoc(new_facing,loc,my,mx)
        if(valid):
            ProcessBeam(new_facing,new_loc,map,d)
        return
    elif((map[y][x].mirror == "/" and (facing == "v")) or
         (map[y][x].mirror == "\\" and (facing == "^"))):
        new_facing = "<"
        (new_loc,valid) = GetNewLoc(new_facing,loc,my,mx)
        if(valid):
            ProcessBeam(new_facing,new_loc,map,d)
        return
    elif((map[y][x].mirror == "/" and (facing == ">")) or
         (map[y][x].mirror == "\\" and (facing == "<"))):
        new_facing = "^"
        (new_loc,valid) = GetNewLoc(new_facing,loc,my,mx)
        if(valid):
            ProcessBeam(new_facing,new_loc,map,d)
        return    
    elif((map[y][x].mirror == "/" and (facing == "<")) or
         (map[y][x].mirror == "\\" and (facing == ">"))):
        new_facing = "v"
        (new_loc,valid) = GetNewLoc(new_facing,loc,my,mx)
        if(valid):
            ProcessBeam(new_facing,new_loc,map,d)
        return    
    return

def ClearBeams(map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            map[y][x].beams = []
    return

if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    map = BuildMap(lines)
#    PrintMap(map)

    max = 0
#    max_loc = (0,0)
    for y in range(len(map)):
        x = 0
        ProcessBeam(">",(y,x),map,0)  # facing, entering (location), map
        val = CountEnergized(map)
        ClearBeams(map)
        if(val > max):
            max = val
            max_loc = (y,x)  # we don't technically need to track this
    for y in range(len(map)):
        x = len(map[0])-1
        ProcessBeam("<",(y,x),map,0)  # facing, entering (location), map
        val = CountEnergized(map)
        ClearBeams(map)
        if(val > max):
            max = val
            max_loc = (y,x)  # we don't technically need to track this    
    for x in range(len(map[0])):
        y = 0
        ProcessBeam("v",(y,x),map,0)  # facing, entering (location), map
        val = CountEnergized(map)
        ClearBeams(map)
        if(val > max):
            max = val
            max_loc = (y,x)  # we don't technically need to track this 
    for x in range(len(map[0])):
        y = len(map)-1
        ProcessBeam("^",(y,x),map,0)  # facing, entering (location), map
        val = CountEnergized(map)
        ClearBeams(map)
        if(val > max):
            max = val
            max_loc = (y,x)  # we don't technically need to track this 

#    energized = PrintEnergized(map)

#    energized = CountEnergized(map)
#    print("Part 1:",energized)
    print("Part 2:",max)




