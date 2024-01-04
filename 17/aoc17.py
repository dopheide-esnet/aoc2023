#!/usr/bin/env python3

import copy

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

class Heat:
    def __init__(self):
        self.min = dict()

def BuildMap(lines):
    heatmap=list()
    map=list()
    for line in lines:
        row = list(line)
        row = [int(i) for i in row if i]
        map.append(row)
        row = list()
        for x in range(len(line)):
            row.append(Heat())
        heatmap.append(list(row))

    return (map,heatmap)

def new_facings(loc,facing,my,mx,depth):

    # Prioritize down and right to try and get to the end faster.

    nf = list()
    (y,x) = loc
    if(facing == ">" or facing == "<"):
        if(y + 1 < my):
            nf.append(["v",(y+1,x)])
        if(y - 1 >= 0):
            nf.append(["^",(y-1,x)])
    if(facing == "^" or facing == "v"):
        if(x + 1 < mx):
            nf.append([">",(y,x+1)])
        if(x - 1 >= 0):
            nf.append(["<",(y,x-1)])
    return(nf)

def CheckFacing(loc,facing,my,mx):
    (y,x) = loc
    if(facing == ">" and x + 1 < mx):
        return (True,(y,x+1))
    elif(facing == "<" and x - 1 >= 0):
        return (True,(y,x-1))
    elif(facing == "^" and y - 1 >= 0):
        return (True,(y-1,x))
    elif(facing == "v" and y+1 < my):
        return (True,(y+1,x))
    return (False,(0,0))

def FindPath(loc,facing,in_a_row,map,heatmap,my,mx,heat,depth,max):

# can't just modify the heatmap because we don't want to keep modified copies
# for bad paths...

    if(depth > 1000):
        print("Stop on depth",loc)
        exit()
        for y in range(len(heatmap)):
            for x in range(len(heatmap[0])):
                min = "x"
                for h in heatmap[y][x].min:
                    if min == 'x':
                        min = heatmap[y][x].min[h]
                    elif heatmap[y][x].min[h] < min:
                        min = heatmap[y][x].min[h]
                print(min," ",end='')
            print()

    # Set a max which would be 9*(width+length)
    # could make this smaller to be more 'reasonable' for efficiency
#    max = 9*(my+mx)


    # increase heat and check heatmap
    (y,x) = loc

    if(depth != 0):
        heat += map[y][x]

#        if(depth == 3):
#            print(y,x,heat)

        if(heat > max):
#            return (False,list())
            return max
        
        if(heat + (my-y) + (mx-x) > max):
            # too far away to complete
            return max

        if((in_a_row,facing) not in heatmap[y][x].min):
            heatmap[y][x].min[(in_a_row,facing)] = heat
        elif(heat > heatmap[y][x].min[(in_a_row,facing)]):   ## need facing and in-a-row???? COME ON!!
#            return (False,list())
            return max
        else:
            heatmap[y][x].min[(in_a_row,facing)] = heat  # new minimum
        
        if(y == my-1 and x == mx-1):
            print("Done",heat)
            if(heat < max):
                return heat
            else:
                return max
#            return (True,heatmap)

# depth first search
# go down a full path, calculate that heat loss.
# go back one step, calculate and compare.
# keep doing that, if any path's heat loss is too high, stop early.
# if a path's full heat loss it less, update that value.

# it would be ideal if we could flip going down and right each turn.

    # Figure out allowed new facings
    if(in_a_row < 2):
        # can continue this facing.  Check boundaries...
        # THIS
        checked = CheckFacing(loc,facing,my,mx)
        if(checked[0]):
            # can still go this way.
            new_max = FindPath(checked[1],facing,in_a_row+1,map,heatmap,my,mx,heat,depth+1,max)
            if(new_max < max):
                max = new_max
#            (good,new_heatmap) = FindPath(checked[1],facing,in_a_row+1,map,copy.deepcopy(heatmap),my,mx,heat,depth+1)
#            if(good):
#                heatmap = new_heatmap # TODO, do we need to update all min elements?
#        AND OR...
    new_facing = new_facings(loc,facing,my,mx,depth)
    for i in range(len(new_facing)):
        # try both new facings, resetting in_a_row to zero
        new_max = FindPath(new_facing[i][1],new_facing[i][0],0,map,heatmap,my,mx,heat,depth+1,max)
        if(new_max < max):
            max = new_max
#        (good,new_heatmap) = FindPath(new_facing[i][1],new_facing[i][0],0,map,copy.deepcopy(heatmap),my,mx,heat,depth+1)
#        if(good):
#            heatmap = new_heatmap

    return max


if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    (map,heatmap) = BuildMap(lines)

#    print(map)
#    print(heatmap)

    my = len(map)
    mx = len(map[0])

    max = 1054 # experimental max.
    facing = ">"
    new_max = FindPath((0,0),facing,0,map,heatmap,my,mx,0,0,max)
    facing = "v"
    new_max = FindPath((0,0),facing,0,map,heatmap,my,mx,0,0,new_max)

    print("new_max",new_max)
    print("Part 1:",heatmap[my-1][mx-1].min)

