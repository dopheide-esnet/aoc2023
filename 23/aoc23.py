#!/usr/bin/env python3

#import sys
#sys.setrecursionlimit(2000)

testcase = True
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def BuildMaze(lines):
    maze = list()
    for line in lines:
        maze.append(list(line))
    return maze

class Segment:
    def __init__(self,start,heading,steps,end):
        self.start = start
        self.heading = heading
        self.steps = steps
        self.end = end

def GetOptions(loc,heading,maze):
    (y,x) = loc
    options = list()
    # Check up
    if(heading != "v"):
        if(y-1 >= 0):
            if(maze[y-1][x] in ['.','^','>','<']):
                options.append('^')
    # Check left
    if(heading != '>'):
        if(x-1 >= 0):
            if(maze[y][x-1] in ['.','^','v','<']):
                options.append('<')
    # Check right
    if(heading != '<'):
        if(x+1 < len(maze[0])):
            if(maze[y][x+1] in ['.','^','v','>']):
                options.append('>')
    # Check down
    if(heading != '^'):
        if(y+1 < len(maze)):
            if(maze[y+1][x] in ['.','v','>','<']):
                options.append('v')
    return options

def Explore(seg_start,head_start,loc,steps,heading,maze,segments):

    (y,x) = loc

    options = [heading]
    while(len(options) == 1):

        heading = options[0]
        # Go down
        if(heading == "v"):
            y = y+1
            steps += 1
            if(y == len(maze)-1):
#                print("Segment",seg_start,(y,x),"steps",steps)
#                print("Found the end!",head_start)
                if(seg_start not in segments):
                    segments[seg_start] = dict()
                segments[seg_start][head_start] = Segment(seg_start,head_start,steps,(y,x))
                
                return
        # Go right
        elif(heading == '>'):
            x = x+1
            steps += 1
        elif(heading == '<'):
            x = x-1
            steps += 1
        elif(heading == '^'):
            y = y-1
            steps += 1
        else:
            print("Unknown heading")
            exit()

        # Check for options
        options = GetOptions((y,x),heading,maze)
    #    print("Options",options)

        if(len(options) == 0):
            print("Dead end, return something?")
            exit()
        elif(len(options) > 1):
            # End of segment
#            print("Segment",seg_start,(y,x),"steps",steps)
            if(seg_start not in segments):
                segments[seg_start] = dict()
            segments[seg_start][heading] = Segment(seg_start,heading,steps,(y,x))


            for heading in options:
# Does this causes problems when one segment meets up with another that was already explored.
# the new one could be shorter?
# Fixing using head_start
                if((y,x) in segments):
                    if(heading in segments[(y,x)]):
                        continue  # we already know about this segment
                Explore((y,x),heading,(y,x),0,heading,maze,segments)
            options = []  # or just break?

        # If len(options) == 1, keep looping.

def FindMaxPath(loc,end_loc,segments):

    possible = list()
    ## If it loops, can't do the same path twice.

    for path in segments[loc]:
        if(segments[loc][path].end == end_loc):
            possible.append(segments[loc][path].steps)
#            print("end")
        else:
            next_loc = segments[loc][path].end
            next_poss = FindMaxPath(next_loc,end_loc,segments)
            for p in range(len(next_poss)):
                next_poss[p] += segments[loc][path].steps
            possible.extend(next_poss)

#    print("Possible",possible)
    return possible


if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    maze = BuildMaze(lines)
    start_position = (0,1)

    # What if we built a dict of path segments.
    # For instance, start (0,1) to (5,3), there are no choices.

    # REMEMBER never step onto the same tile twice.

    segments = dict()
    Explore(start_position,"v",start_position,0,"v",maze,segments)

    end_position = (len(maze)-1,maze[len(maze)-1].index("."))
    print("End at",end_position)

    result = FindMaxPath(start_position,end_position,segments)
    print(max(result))

#    for m in maze:
#        print("".join(m))

#    for y in range(len(maze)):
#        for x in range(len(maze[0])):
#            if(y == 13 and x == 13):
#                print("M",end='')
#            else:
#                print(maze[y][x],end='')
#        print()




