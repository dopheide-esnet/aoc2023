#!/usr/bin/env python3

testcase = True
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def BuildMap(lines,plots):
    map = list()
    y=0
    for line in lines:
        map.append(list(line))
        if('S' in map[y]):
            x = map[y].index('S')
            plots[(y,x)] = 1
            map[y][x] = '.'  # make it a workable plot
        y+=1
    return map


def WalkThisWay(map,plots):
    # map just serves as a reference for where the rocks are and where you can't go.
    new_plots = dict()   # so inefficient, lay off.  this way we don't have to remember to delete where we were

    for (y,x) in plots:
        # try north,west,east,south
        if(y != 0):
            if map[y-1][x] == '.':
                new_plots[(y-1,x)] = 1
        if(y < len(map)-1):
            if map[y+1][x] == '.':
                new_plots[(y+1,x)] = 1
        if(x != 0):
            if map[y][x-1] == '.':
                new_plots[(y,x-1)] = 1
        if(x < len(map[0])-1):
            if map[y][x+1] == '.':
                new_plots[(y,x+1)] = 1
    return new_plots

if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    # *sigh* do it the dumb way first...
    plots = dict()
    map = BuildMap(lines,plots)
#    print(map)
#    print(plots)

    steps = 64
    for s in range(steps):
        plots = WalkThisWay(map,plots)

    print(len(plots))



