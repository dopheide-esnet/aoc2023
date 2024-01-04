#!/usr/bin/env python3

# Modified for Big Crucible

import copy

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

heatmap=list()

class Heat:
    def __init__(self):
        self.min = dict()

def BuildMap(lines):
    global heatmap
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

def new_facings(loc,facing,my,mx,depth,iar):
    # Prioritize down and right to try and get to the end faster.

    nf = list()
    (y,x) = loc
    if(facing == ">" or facing == "<"):
        if(y + (4-iar) < my and y+1<my):
            nf.append(["v",(y+1,x)])
        if(y - (4-iar) >= 0 and y-1 >= 0):
            nf.append(["^",(y-1,x)])
    if(facing == "^" or facing == "v"):
        if(x + (4-iar)< mx and x+1<mx):
            nf.append([">",(y,x+1)])
        if(x - (4-iar) >= 0 and x-1 >= 0):
            nf.append(["<",(y,x-1)])
    return(nf)

    # Let's try changing this.  Perhaps we're going too deep too many times when
    # we should be eliminating possibilities earlier.

    nf = list()
    (y,x) = loc
    if(facing == ">" or facing == "<"):
        if(y - 1 >= 0):
            nf.append(["^",(y-1,x)])
        if(y + 1 < my):
            nf.append(["v",(y+1,x)])
    if(facing == "^" or facing == "v"):
        if(x - 1 >= 0):
            nf.append(["<",(y,x-1)]) 
        if(x + 1 < mx):
            nf.append([">",(y,x+1)])
   
    return(nf)
    



def CheckFacing(loc,facing,my,mx,iar):
    # iar = in_a_row value
    # no point in going towards an edge if we haven't moved far enough to turn.
    (y,x) = loc
    if(facing == ">" and x + (4-iar) < mx and x + 1 < mx):
        return (True,(y,x+1))
    elif(facing == "<" and x - (4-iar) >= 0 and x - 1 >=0):
        return (True,(y,x-1))
    elif(facing == "^" and y - (4-iar) >= 0) and y - 1 >=0:
        return (True,(y-1,x))
    elif(facing == "v" and y + (4-iar) < my and y+1 < my):
        return (True,(y+1,x))
    return (False,(0,0))




def FindPath(loc,facing,in_a_row,map,my,mx,heat,depth,max):
    global heatmap
# can't just modify the heatmap because we don't want to keep modified copies
# for bad paths...

# EXTRA TODO:  Should we remove going 'backwards' (^ or <) too far or too many times?

#  TODO, for part 2,
#      we have to be moving in a straight line for a few points before ending.
#      so that changes our potential end conditions

    if(depth > 400):
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

# NEW TODO.  Could break on routes that are too far away to get to the end before the max.


    # increase heat and check heatmap
    (y,x) = loc

    if(depth != 0):
        heat += map[y][x]

#        if(depth == 3):
#            print(y,x,heat)

# POSSIBLE BREAK
### what if we only track facing and not in_a_row...
# it is faster... not sure if it's a accurate.
#        if(facing not in heatmap[y][x].min):
#            heatmap[y][x].min[facing] = heat
#        elif(heat > heatmap[y][x].min[facing]):   ## need facing and in-a-row???? COME ON!!

#            return max
#        else:
#            heatmap[y][x].min[facing] = heat  # new minimum to get here with this facing


        if((in_a_row,facing) not in heatmap[y][x].min):
            heatmap[y][x].min[(in_a_row,facing)] = heat
        elif(heat > heatmap[y][x].min[(in_a_row,facing)]):   ## need facing and in-a-row???? COME ON!!
            return max
        else:
            heatmap[y][x].min[(in_a_row,facing)] = heat  # new minimum to get here with this facing

# END POSSIBLE BREAK

        if(heat > max):
#            print("hit fake max")
#            return (False,list())
            return max

        if(heat + (my-y) + (mx-x) > max):
            # too far away to complete
            return max

        # what about a check for... if the distance I've traveled from the middle
        # isn't more than a rough average....
    # TODO Part 2:  I think this won't work in part 2
        if(heat > (y + x) * 6):  # guessing 6 is too much.
            return max

        if(y == my-1 and x == mx-1):
            if(in_a_row >= 4):
                print("Done",heat,depth)
                if(heat < max):
                    return heat
                else:
                    return max
            else:
                print("Shouldn't get here, end without sufficient run")
                exit()
#            return (True,heatmap)

    # Figure out allowed new facings

    skipturns = False
    if(in_a_row < 4):
        skipturns = True
        # MUST continue this facing if it's not a dead end.

    if(in_a_row < 10):  # do we have the 3 and 9 correct?
        # can continue this facing.  Check boundaries...
        # THIS
        checked = CheckFacing(loc,facing,my,mx,in_a_row)
        if(checked[0]):
            # can still go this way.
            new_max = FindPath(checked[1],facing,in_a_row+1,map,my,mx,heat,depth+1,max)
            if(new_max < max):
                max = new_max

    if(skipturns == False):
        new_facing = new_facings(loc,facing,my,mx,depth,in_a_row)
        for i in range(len(new_facing)):
            # try both new facings, resetting in_a_row to zero
            new_max = FindPath(new_facing[i][1],new_facing[i][0],1,map,my,mx,heat,depth+1,max)
            if(new_max < max):
                max = new_max

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

    max = 1200 # experimental max.  

    facing = ">"
    new_max = FindPath((0,0),facing,1,map,my,mx,0,0,max)
    facing = "v"
    new_max = FindPath((0,0),facing,1,map,my,mx,0,0,new_max)

    print("new_max",new_max)
    print("Part 1:",heatmap[my-1][mx-1].min)

