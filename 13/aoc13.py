#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def BuildFields(lines):
    maps = list()
    reading = True
    y=0
    new_map = list()
    for line in lines:
        if(len(line)) == 0:
            maps.append(new_map)
            y = 0
            new_map=list()
            continue
        new_map.append(list(line))
        y+=1
    maps.append(new_map)
    return maps

def FindMirror(map):
    # mirror line can't be on either edge
    # Horizontal
    orig_y=-1
    orig_x=-1
    for y in range(1,len(map)):

        potential=True
        for x in range(len(map[y])):
            if(map[y-1][x] != map[y][x]):
                potential=False
                break
        if(not potential):
            continue
#        print("Potential at",y)
        i = 1
        # now need to check the y's at it expands out.
        while(y-1-i >= 0 and y+i < len(map)):
            for x in range(len(map[y])):
                if(map[y-1-i][x] != map[y+i][x]):
                    potential=False
                    break
            i+=1
        if(potential == True):
            print("We found the original y",y)
#            return y*100
            orig_y = y

    ### IF potential is still False, look for X?
    # then do smudge searches
    if(not potential):

        # Vertical
        for x in range(1,len(map[0])):
            potential = True
            for y in range(len(map)):
                if(map[y][x-1] != map[y][x]):
                    potential = False
                    break
            if(not potential):
                continue
            i = 1
            while(x-1-i >= 0 and x+i < len(map[0])):
                for y in range(len(map)):
                    if(map[y][x-1-i] != map[y][x+i]):
                        potential = False
                        break
                i += 1
            if(potential == True):
                print("We found original x",x)
                orig_x = x
    #            return x 

    ## Smudges Y
    for y in range(1,len(map)):
        if(y == orig_y):  # we know the reflection line isn't at y with the smudge.
            continue
        potential=True
        sm = 0
        smudge = list()

        for x in range(len(map[y])):
            if(map[y-1][x] != map[y][x]):
                if(sm == 0):  # we only allow 1 smudge, but could be either location
                    sm = 1
                    smudge.append((y-1,x))  # possible smudge location
                    smudge.append((y,x))
                else:
                    potential=False
                    break
        if(not potential):
            continue
        print("Potential at",y)
        i = 1
        # now need to check the y's at it expands out.
        while(y-1-i >= 0 and y+i < len(map)):
            for x in range(len(map[y])):
                if(map[y-1-i][x] != map[y+i][x]):
                    # TODO, if we don't have a smudge yet, it could be out here somewhere.
                    if(sm == 0):
                        sm = 1
                        smudge.append((y-1-i,x))
                        smudge.append((y+i,x))
                    else:
                        potential=False
                        break
            i+=1
        if(potential == True):
            print("y We found it!",y)
            return y*100


    # Smudges X
    for x in range(1,len(map[0])):
        if(x == orig_x):  # we know the reflection line isn't at y with the smudge.
            continue
        sm = 0
        smudge = list()
        potential = True

        for y in range(len(map)):
            if(map[y][x-1] != map[y][x]):
                if(sm == 0):  # we only allow 1 smudge, but could be either location
                    sm = 1
                    smudge.append((y,x-1))  # possible smudge location
                    smudge.append((y,x))
                else:
                    potential=False
                    break
        if(not potential):
            continue
        i = 1
        while(x-1-i >= 0 and x+i < len(map[0])):
            for y in range(len(map)):
                if(map[y][x-1-i] != map[y][x+i]):
                    if(sm == 0):
                        sm = 1
                        smudge.append((y,x-1-i))
                        smudge.append((y,x+1))
                    else:
                        potential=False
                        break
            i += 1
        if(potential == True):
            print("We found it! x",x)
            return x

    for m in map:
        print("".join(m))
#    print(map)
    print("Shouldn't get here")
    exit()


if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    maps = BuildFields(lines)
    total = 0
    for m in maps:
        total += FindMirror(m)
    print("Part 1:",total)

