#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def GetGalaxies(lines):
    y = 0
    ygal = []
    xgal = []
    map = []
    for line in lines:
        chars = list(line)
        for x in range(len(chars)):
            if(chars[x] == '#'):
                map.append((y,x))
                if(y not in ygal):
                    ygal.append(y)
                if(x not in xgal):
                    xgal.append(x)
        y+=1
    return(map,xgal,ygal)

def ExpandY(map,ygal,ymax):
    # for each subsequent expansion, take into consideration the previous one.
    expansions = 0
    factor = 999999
    for y in range(ymax):
        if(y not in ygal):
            # expand here
            for i in range(len(map)):
                (my,mx) = map[i]
                if( my > (y+(expansions * factor))):
                    map[i] = (my+factor,mx)
            expansions += 1        
    print("Y expansions:",expansions)

def ExpandX(map,xgal,xmax):
    # for each subsequent expansion, take into consideration the previous one.
    expansions = 0
    factor = 999999
    for x in range(xmax):
        if(x not in xgal):
            # expand here
            for i in range(len(map)):
                (my,mx) = map[i]
                if( mx > (x+(expansions*factor))):
                    map[i] = (my,mx+factor)
            expansions += 1        
    print("X expansions:",expansions)

if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    (map,xgal,ygal) = GetGalaxies(lines)

    # modified for Part 2
    ExpandY(map,ygal,len(lines))
    ExpandX(map,xgal,len(lines[0]))

    # map elements are not sorted in any way.
    total = 0
    for i in range(len(map)):
        for j in range(i+1,len(map)):
            (iy,ix) = map[i]
            (jy,jx) = map[j]
            diff = abs(jy-iy) + abs(jx-ix)
            total += diff
    print(total)





