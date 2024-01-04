#!/usr/bin/env python3

import copy
#import sys
#sys.setrecursionlimit(2000)

# Modified for Part 2

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
            if(maze[y-1][x] in ['.','^','>','<','v']):
                options.append('^')
    # Check left
    if(heading != '>'):
        if(x-1 >= 0):
            if(maze[y][x-1] in ['.','^','v','<','>']):   # > is now an option, but don't want to go backwards
                options.append('<')
    # Check right
    if(heading != '<'):
        if(x+1 < len(maze[0])):
            if(maze[y][x+1] in ['.','^','v','>','<']):
                options.append('>')
    # Check down
    if(heading != '^'):
        if(y+1 < len(maze)):
            if(maze[y+1][x] in ['.','v','>','<','^']):
                options.append('v')

    # For Part 2, don't go backwards now that we've added more options above.
    if(heading == 'v'):
        if('^' in options):
            options.remove('^')
    elif(heading == '>'):
        if('<' in options):
            options.remove('<')
    elif(heading == '<'):
        if('>' in options):
            options.remove('>')
    elif(heading == '^'):
        if('v' in options):
            options.remove('^')

    return options

def Explore(seg_start,head_start,loc,steps,heading,maze,segments,exploring):

    (y,x) = loc
#    print("Exploring from",y,x,heading)
    if((loc,heading) in exploring):
        return
    exploring.append((loc,heading))

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
#            print("Dead end, return something?",(y,x))
            return
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
                Explore((y,x),heading,(y,x),0,heading,maze,segments,exploring)
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


def FindMaxPath2(loc,end_loc,segments,history):
    possible = list()
    history.append(loc)  # can't go back here.

    for path in segments[loc]:
        if(segments[loc][path].end == end_loc):
            possible.append(segments[loc][path].steps)        
        else:
            next_loc = segments[loc][path].end
            if(next_loc not in history):
                next_poss = FindMaxPath2(next_loc,end_loc,segments,copy.copy(history))
                for p in range(len(next_poss)):
                    next_poss[p] += segments[loc][path].steps
                possible.extend(next_poss)
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
    exploring = []
    Explore(start_position,"v",start_position,0,"v",maze,segments,exploring)

    end_position = (len(maze)-1,maze[len(maze)-1].index("."))
    print("End at",end_position)

#    for m in maze:
#        print("".join(m))

#    for y in range(len(maze)):
#        for x in range(len(maze[0])):
#            if(y == 125 and x == 133):
#                print("M",end='')
#            else:
#                print(maze[y][x],end='')
#        print()


#    result = FindMaxPath(start_position,end_position,segments)
#    print(max(result))

# For Part2, I _think_ all the segments are correct, they can just be interpreted both ways now.

    # can we just find all possible non-overlapping paths?
    # this means you can't even go back to the same junction twice, but you
    # can go from an end to a start.

    # perhaps re-populate a new 'segments' with the reverse paths available.
    tmp_dict = dict()
    for s in segments:
        for h in segments[s]:
            seg_start = segments[s][h].end
            heading = segments[s][h].heading + "r" # actually original heading, but whatever
            if(seg_start not in tmp_dict):
                tmp_dict[seg_start] = dict()
            tmp_dict[seg_start][heading] = Segment(seg_start,heading,segments[s][h].steps,segments[s][h].start)
            # this right?
    # merge back into segments
    for t in tmp_dict:
        if t not in segments:
            segments[t] = dict()
        for h in tmp_dict[t]:
            if(h not in segments[t]):
                segments[t][h] = tmp_dict[t][h]

    history = []

    for s in segments:
        for h in segments[s]:
            print(segments[s][h].start,h,segments[s][h].end)

    result = FindMaxPath2(start_position,end_position,segments,history)
    print(max(result))

# I think we're going to have to re-explore and not ignore slope options to find all the intersections












