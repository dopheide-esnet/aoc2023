#!/usr/bin/env python3


testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def ProcessInstruction2(loc,line,map):
    (facing,count,color) = line.split(" ")
    count = int(count)
#    print(facing,count,color)

    (y,x) = loc
    if(facing == "R"):
        while(count > 0):
            x += 1  # new x index
            if(x == len(map[y])):
                # we're at the end of the row, just append
                map[y].append('#')
            elif(x > len(map[y])):
                start = len(map[y])
                while(start < x):
                    map[y].append('.')
                    start += 1
            else:
                map[y][x] = '#'  # overwrite whatever is there.
            count -= 1
    elif(facing == "D"):
        while(count > 0):
            y += 1
            if(y == len(map)):
                new_row = list()
                map.append(new_row)

            # existing row, but stuff up to 'x' location may not exist.
            # need to populate from len(map[y]) to x - 1
            start = len(map[y])
            while(start < x):
                map[y].append('.')
                start += 1
            map[y].append('#')
            count -= 1
    elif(facing == "L"):
        while(count > 0):
            x -= 1
            map[y][x] = '#'
            count -= 1
    elif(facing == "U"):
        while(count > 0):
            y -= 1
            map[y][x] = '#'
            count -= 1
    return (y,x)

def ProcessInstructions(lines):
    map = list()
    y = 0
    x = 0
    my = 0
    mx = 0
    miny = 0
    minx = 0
    # Find extents to build the map

    for line in lines:
        (facing,count,color) = line.split(" ")
        count = int(count)
        if(facing == 'R'):
            x += count
            if(x > mx):
                mx = x
        elif(facing == 'L'):
            x -= count
            if(x < minx):
                minx = x
        elif(facing == 'U'):
            y -= count
            if(y < miny):
                miny = y
        else:
            y += count
            if(y > my):
                my = y
    print(my,mx,miny,minx)

    row = '.' * (mx+abs(minx)+1)
    for y in range(my+abs(miny)+1):
        map.append(list(row))

    y = 357   # new origin
    x = 201
    map[y][x] = "#"
    l = 0
    for line in lines:
        l += 1
        (facing,count,color) = line.split(" ")
        count = int(count)
        if(facing == 'R'):
            while(count > 0):
                x += 1
                map[y][x]='#'
                count -= 1
        elif(facing == 'L'):
            while(count > 0):
                x -= 1
                map[y][x]='#'
                count -= 1            
        elif(facing == 'U'):
            while(count > 0):
                y -= 1
                if(y < 0):
                    print("wtf",l)
                    exit()
                map[y][x]='#'
                count -= 1    
        else:
            while(count > 0):
                y += 1
                map[y][x]='#'
                count -= 1  
    return map

def FillIn(map):
    total = map[0].count('#')
    total += map[len(map)-1].count('#')

    for y in range(1,len(map)-1):
        row_total = 0
        inside = False
        up_down = (0,0)
        for x in range(len(map[y])):
            # need to check for full 'crossings'
            
            ## We could have empty space above or below.
            if(map[y][x] == '#'):
                row_total += 1

                if(not ((len(map[y-1]) <= x) or (len(map[y+1]) <= x))):
                    if(map[y-1][x] == "#" and map[y+1][x] == "#"):
                        inside = not inside                
                        continue
                if(x < len(map[y-1])):
                    if(map[y-1][x] == "#"):
                        if(up_down == (0,1)):
                            inside = not inside
                            up_down = (0,0)
                        elif(up_down == (1,0)):  # U-turn
                            up_down = (0,0)
                        else:
                            up_down = (1,0)
                        continue
                if(not len(map[y+1]) <= x):
                    if(map[y+1][x] == "#"):
                        if(up_down == (1,0)):
                            inside = not inside
                            up_down = (0,0)
                        elif(up_down == (0,1)):  # U-turn
                            up_down = (0,0)
                        else:
                            up_down = (0,1) 
                        continue                                       
            else:
                if(inside):
                    row_total += 1

#                ould have #   ##   #    or #     # #    #
#                or ##    ##  
                # no flipping


#        row_total += len(all)
        total += row_total 
#        print("row",y,":",row_total)
#        exit()

#        for x in range(len(map[y])):  # must be len at 'y', all rows aren't equal in length
    return total

def GetCoordinates(lines):
    instructions = list()
    coords = list()
    x = 0
    y = 0
    total_count=0

    for line in lines:
        (facing,count,color) = line.split(" ")
        # convert hex to int
        facing = int(color[7])
        color = color[2:7]
#        count = int(count)
        count = int(color,16)
        if(facing == 0): # R
            facing = 'R'
        elif(facing == 1): # D
            facing = 'D'
        elif(facing == 2): # L
            facing = 'L'
        elif(facing == 3): # U
            facing = 'U'

        instructions.append((facing,count))

#    print(instructions)

    for i in range(len(instructions)):
        (facing,count) = instructions[i]
        if(i == len(instructions) - 1):
            (next_facing, trash) = instructions[0]
        else:
            (next_facing, trash) = instructions[i+1]
        if(i == 0):
            (prev_facing, trash) = instructions[-1]
        else:
            (prev_facing, trash) = instructions[i-1]

        if(facing == 'R'): # R
            if(next_facing == 'D' and prev_facing=='U'):
                x += count + 1
            elif(next_facing == 'U' and prev_facing=='D'):
                x += count - 1
            else:
                x += count  # right?

        elif(facing == 'D'): # D
            if(next_facing == 'L' and prev_facing == 'R'):
                y -= count + 1
            elif(next_facing == 'R' and prev_facing == 'L'):
                y -= count - 1
            else:
                y -= count

        elif(facing == 'L'): # L
            if(next_facing == 'D' and prev_facing =='U'):
                x -= count - 1
            elif(next_facing == 'U' and prev_facing == 'D'):
                x -= count + 1
            else:
                x -= count

        elif(facing == 'U'): # U
            if(next_facing == 'L' and prev_facing == 'R'):
                y += count - 1
            elif(next_facing == 'R' and prev_facing == 'L'):
                y += count + 1
            else:
                y += count

        total_count += count
        coords.append((x,y))

    return coords


if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()


    coords = GetCoordinates(lines)

    ##  need to keep track of where the dug hole is in relation to the coordinate

    print(coords)

    # shoelace formula for polygon area calculation

    # The Test case should end up with these:
#    coords = [(0, 0), (7,0), (7,-6), (5,-6), (5,-7), (7,-7), (7,-10),(1,-10),(1,-8),(0,-8),(0,-5),(2,-5),(2,-3),(0,-3)]

    total = 0
    for i in range(len(coords)):
#        print(coords[i])
        (x1,y1) = coords[i]
        if(i < len(coords) - 1):            
            (x2,y2) = coords[i+1]
        else:
            (x2,y2) = coords[0]
        val = (x1 * y2) - (x2 * y1)
        total += val

    print((abs(total) / 2))
    # add all the distances to it?

    exit()
    map = ProcessInstructions(lines)
    print("Part 1:",FillIn(map))



#    for m in map:
#        print("".join(m),end='')
#        print()
