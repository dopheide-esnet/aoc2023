#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test2.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def BuildMap(lines):
    map = dict()
    y = 0
    for line in lines:
        chars = list(line)
        for x in range(len(chars)):
            char = chars[x]
            if(char == "|"):
                connects = [(y-1,x),(y+1,x),char]
            elif(char == "-"):
                connects = [(y,x-1),(y,x+1),char]
            elif(char == "L"):
                connects = [(y-1,x),(y,x+1),char]
            elif(char == "J"):
                connects = [(y-1,x),(y,x-1),char]
            elif(char == "7"):
                connects = [(y+1,x),(y,x-1),char]
            elif(char == "F"):
                connects = [(y+1,x),(y,x+1),char]
            elif(char == "."):
                connects = []
            elif(char == "S"):
                start = (y,x)  # we'll determine it's shape later cause we need the full map
            map[(y,x)] = connects
        y += 1
    return (start,map)

def GetStartShape(start,map):
    (y,x) = start
    connects = []
    # north works
    if((y-1,x) in map and start in map[(y-1,x)]):
        # north works
        connects.append((y-1,x))
        # |
        if(map[(y+1,x)] and start in map[(y+1,x)]):
            connects.append((y+1,x))
            connects.append("|")
        # L
        elif(map[(y,x+1)] and start in map[(y,x+1)]):
            connects.append((y,x+1))
            connects.append("L")
        # J
        elif(map[(y,x-1)] and start in map[(y,x-1)]):
            connects.append((y,x-1))
            connects.append("J")
    # south works
    elif(map[(y+1,x)] and start in map[(y+1,x)]):
        connects.append((y+1,x))
        # F
        if(map[(y,x+1)] and start in map[(y,x+1)]):
            connects.append((y,x+1))
            connects.append("F")
        # 7
        elif(map[(y,x-1)] and start in map[(y,x-1)]):
            connects.append((y,x-1))
            connects.append("7")
    else:
        connects = [(y,x-1),(y,x+1),"-"]
    map[start] = connects

def FindLoop(start,map):
    loop = []  # for part2
    steps = 1
    # just pick a direction:
    prev = start
    loop.append(prev)
    loc = map[start][0]
    while(loc != start):
        if(map[loc][0] == prev):
            # go the other way
            prev = loc
            loc = map[loc][1]
        else:
            prev = loc
            loc = map[loc][0]
        loop.append(prev)
        steps += 1

    return (loop)

if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    (start,map) = BuildMap(lines)
    GetStartShape(start,map)
#    print(start,map)
#    print(map[start])

    loop = FindLoop(start,map)
    print(len(loop)/2)

    # need to mark all tiles that aren't part of the loop.
    # easier to mark the ones that are first.

    #Could you calculate "inside" by the number of loop lines per row?
    # or every two you are either inside or outside?

    # But don't count horizontals "-" as inverting the in/out state?
    print("Grid Size",len(lines),len(lines[0]))
    total=0
    for y in range(len(lines)):
        inside = False
        predir = None
        dir = None
        # go from left.. go from right
        xstart = -1
        for x in range(len(lines[0])):
            if((y,x) in loop):
                xstart = x
                break
        for x in reversed(range(len(lines[0]))):
            if (y,x) in loop:
                xend = x
                break
        if(xstart != -1):
            print("X",xstart,xend)
            print("Ts:",total)

            # have to keep track of up/down, ignore dashes.
            # each pair flips 'inside' state

            # dammit, go back and keep track of shape.

            for x in range(xstart,xend):
                if (y,x) in loop:
                    shape = map[y,x][2]
                    if(shape != "-"):  # not a dash
                        if(shape == "|"):
                            inside = not inside
                        elif(predir == None):
                            predir = shape
                        elif((predir == "L" and shape == "7") or 
                             (predir == "7" and shape == "L") or 
                             (predir == "J" and shape == "F") or
                             (predir == "F" and shape == "J")):
                            inside = not inside
                        elif((predir == "L" and shape == "J") or 
                             (predir == "J" and shape == "L") or 
                             (predir == "F" and shape == "7") or
                             (predir == "7" and shape == "F")):
                            predir = None
                        else:
                            predir = shape
                        # need to know if it's opposite the previous up/down
                else:                    
                    if(inside):
                        total += 1
            print("Te:",total)
    print("Total:",total)



    
