#!/usr/bin/env python3

import copy

testcase = False
if testcase:
#    ends = [10,10,10,14]
    ends = [10,10,10,10]
    file = "test2.txt"
    # test case:
#    steady_even = 42
#    steady_odd = 39
    steady_even = 47
    steady_odd = 44

else:
    ends = [130,130,130,130]
    file = "input.txt"
    steady_even = 7592
    steady_odd = 7498
#    steady_odd = 7592
#    steady_even = 7498

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

def CheckEnds(new_y,new_x,ends):
    if(new_y==0 and new_x==0 and ends[0] == -1):
        ends[0] = steps
    elif(new_y==0 and new_x==len(map[0])-1 and ends[1] == -1):
        ends[1] = steps
    elif(new_y==len(map)-1 and new_x==0 and ends[2] == -1):
        ends[2] = steps
    elif(new_y==len(map)-1 and new_x==len(map[0])-1 and ends[3] == -1):
        ends[3] = steps

def WalkThisWay2(map,plots,ends,steps):
    # map just serves as a reference for where the rocks are and where you can't go.
    new_plots = dict()   # so inefficient, lay off.  this way we don't have to remember to delete where we were

    for (y,x) in plots:
        # try north,west,east,south
        if(y != 0):
            if map[y-1][x] == '.':
                new_plots[(y-1,x)] = 1
                new_y = y-1
                new_x = x
                CheckEnds(new_y,new_x,ends)
        if(y < len(map)-1):
            if map[y+1][x] == '.':
                new_plots[(y+1,x)] = 1
                new_y = y+1
                new_x = x
                CheckEnds(new_y,new_x,ends)
        if(x != 0):
            if map[y][x-1] == '.':
                new_plots[(y,x-1)] = 1
                new_y = y
                new_x = x-1
                CheckEnds(new_y,new_x,ends)
        if(x < len(map[0])-1):
            if map[y][x+1] == '.':
                new_plots[(y,x+1)] = 1
                new_y = y
                new_x = x+1
                CheckEnds(new_y,new_x,ends)
        
    return new_plots

def TripleMap(map,plots):
    # initial start spot needs to move to the middle
    for spot in plots:
        (y,x) = spot
    del plots[(y,x)]
    y += len(map)
    x += len(map[0])
    plots[(y,x)] = 1

    add_y = len(map)
    for y in range(len(map)):
        map[y] = map[y]*3
    map = map*3
    return map

def NineMap(map,plots):
    # initial start spot needs to move to the middle
    for spot in plots:
        (y,x) = spot
    del plots[(y,x)]
    y += len(map) * 4
    x += len(map[0]) * 4
    plots[(y,x)] = 1

    add_y = len(map)

    for y in range(len(map)):
        map[y] = map[y]*9

    new_map = []
    for i in range(9):
        for y in range(len(map)):
            new_map.append(copy.copy(map[y]))

    return new_map

def NineTeenMap(map,plots):
    # initial start spot needs to move to the middle
    for spot in plots:
        (y,x) = spot
    del plots[(y,x)]
    y += len(map) * 9
    x += len(map[0]) * 9
    plots[(y,x)] = 1

    add_y = len(map)

    for y in range(len(map)):
        map[y] = map[y]*19

    new_map = []
    for i in range(19):
        for y in range(len(map)):
            new_map.append(copy.copy(map[y]))

    return new_map

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
    cplots = copy.copy(plots)
#    print(map)
#    print(plots)

#    steps = 64
#    for s in range(steps):
#        plots = WalkThisWay(map,plots)

#    print(len(plots))

    # Part 2.  Does the fact that we have a clean 'border' of garden plots help?
    # Seems like a 'full' map repeats every other step.
    # But once we spread out, will they collapse to be totally full?

    # If not, maybe we can calculate how soon a step gets to an edge and how quickly that will cause it to fill
    # the next map..  all 'inside' maps no longer need any calculation.

    # Let's try a 3x3 grid the dumb way and see what the pattern looks like.
#    map = TripleMap(map,plots)
    
#    plots = {(0,0): 1,(len(map)-1,0): 1}

    # The maps straight orthanogally up/down could have multiple entry points?  
    # Or is that impossible just based how how things multiply?
    # maybe if there was a huge rock wall in the way that forces a split?

#.................................
#...................O.............
#.....###.#......###.#......###.#.
#.###.##..#.O###.##.O#..###.##..#.

#...................O.............
#..................O.O............
#.....###.#.O....###O#......###.#.

#..................O.O............
#...........O.....O.O.O...........
#.....###.#O.O...###.#......###.#.

# but we're still coming in from the same side...
# it won't "fill" any faster, but it might matter for final edge calculation.

# So we need to know how many steps it takes to get across the map from any given starting position and what the first
# 'out' step is from there?

# from any given 'entry' point, what is the first exit position on the other sides?
# (we'll also need to know the exist of the central location)

    if(False):
#            ends = [-1,-1,-1,-1] # top,bottom,left,right (they will be (y,x) tuples
        ends = [-1,-1,-1,-1] # steps to NW,NE,SW,SE corners
        steps = 0
        while(-1 in ends):
            steps+=1
            plots = WalkThisWay2(map,plots,ends,steps)
        print(ends)
        print(plots[(0,0)])

        # I calculate all of the 'ends to be == 130 steps once already on the corner (131 total), is that correct?'
        # THIS WILL NOT WORK FOR THE TEST CASE, IT'S DIAGONALS ARE DIFFERENT

#  It seems like it pretty quickly diverts to the clear borders.
#  So..
#  1) we need to know the number of steps from the starting position
#  to each corner.
#  2) we need to know the two steady state counts.
#     7592 at 132 steps (actually first happens at 130 steps) or 131 if you count the first step onto the parsel
#     7498 at 133 steps

#  3) We need to know how many plots there are at each step with a starting position from each corner
#    3b)  And how long until we reach steady-state when starting from each corner.
#
#    4) Note, steady state time is not the time is takes to traverse to the next edge or far corner.
#        (Huh, or maybe it is for the far corner case)

#    5) The 'shape' of the final map is a diamond


    steady_state_steps = (len(map)-1)*2
    print("Steady state:",steady_state_steps)

    if(True):

        southeast = [1] # at step 0 there is 1 plot
        plots = {(0,0): 1} # start top left
        for s in range(1,steady_state_steps+1):
            plots = WalkThisWay(map,plots)
            southeast.append(len(plots))

        southwest = [1] # at step 0 there is 1 plot
        plots = {(0,len(map[0])-1): 1} 
        for s in range(1,steady_state_steps+1):
            plots = WalkThisWay(map,plots)
            southwest.append(len(plots))

        northeast = [1] # at step 0 there is 1 plot
        plots = {(len(map)-1,0): 1} 
        for s in range(1,steady_state_steps+1):
            plots = WalkThisWay(map,plots)
            northeast.append(len(plots))

        northwest = [1] # at step 0 there is 1 plot
        plots = {(len(map)-1,len(map[0])-1): 1} 
        for s in range(1,steady_state_steps+1):
            plots = WalkThisWay(map,plots)
            northwest.append(len(plots))

        # the straight orthagonal direction ends have two starting points.
        south = [1]
        plots = {(0,int(ends[0]/2)): 1}
        for s in range(1,steady_state_steps+1):
            plots = WalkThisWay(map,plots)

            south.append(len(plots))
#        print(south)

        north = [1]
        plots = {(len(map)-1,int(ends[0]/2)): 1}
        for s in range(1,steady_state_steps+1):
            plots = WalkThisWay(map,plots)
            north.append(len(plots))
#        print(north)

        west = [1]
        plots = {(int(ends[0]/2),len(map[0])-1): 1}
        for s in range(1,steady_state_steps+1):
            plots = WalkThisWay(map,plots)
            west.append(len(plots))
#        print(west)

        east = [1]
        plots = {(int(ends[0]/2),0): 1}
        for s in range(1,steady_state_steps+1):
            plots = WalkThisWay(map,plots)          
            east.append(len(plots))
#        print(east)

        # then start doing MATH
        # keep in mind the test case initial diagonals are not equal
        # they are [10,10,10,14]

    # also, in steady state, every other grid is in the opposite of the two states.
    # even: 7592, odd: 7498
    # test case:
    # even: 42 odd: 39

    if(False):
        for s in range(10):
            plots = WalkThisWay(map,plots)
        print("Actual:",len(plots))

    if(True):
        steps = 26501365

        # northwest
        nw_steps = steps - ends[0]

        full_gardens = int(nw_steps / len(map))
        remainder = nw_steps % len(map) # total distance per garden

        print("Full NW:",full_gardens)
          # TODO how to determine which steady state we're at?
        print("remainder:",remainder)
        print(full_gardens,"mid steps:",remainder+len(map)-2) # from 'northwest group'
        print(full_gardens+1,"long steps:",remainder - 2)


        print("TODO, num of 'orthogonal' fulls will be different now")


        if(steps % 2 == 0):
            even = True # which steady state position are we on next (start opposite)
        else:
            even = False

        even_full = 0
        odd_full = 0

        one_diag = 0
        two_diag = 0

        diag = full_gardens - 1

        orig_even = even

        flip = even
        # this depends on even/odd of full_gardens as well

        while(diag > 0):
            if(full_gardens % 2 == 0):
                if(flip):
                    even_full += diag * 4
                    flip = not flip
                else:
                    odd_full += diag * 4
                    flip = not flip
            else:
                if(flip):
                    odd_full += diag * 4
                    flip = not flip
                else:
                    even_full += diag * 4
                    flip = not flip
            diag -= 1


        if(full_gardens % 2 == 0):
            even_full += (full_gardens / 2) * 4
            odd_full += (full_gardens / 2) * 4
        else:
            if(orig_even):
                even_full += int(full_gardens / 2) * 4
                odd_full += (int(full_gardens / 2) + 1) * 4
            else:
                odd_full += int(full_gardens / 2) * 4
                even_full += (int(full_gardens / 2) + 1) * 4

        partial = False
#        if(len(map)+remainder < steady_state_steps):
#            partial = True
#            print("Partial Fulls!")
#            if(full_gardens % 2 == 0):
#                if(orig_even):
#                    even_full -= 4
#                else:
#                    odd_full -= 4
#            else:
#                if(orig_even):
#                    odd_full -= 4
#                else:
#                    even_full -= 4

        # which one is the starting (middle) garden?
        if(even):
            even_full += 1
        else:
            odd_full += 1


        print("Odd Full:",odd_full)
        print("Even Full:",even_full)

        odd_calc = odd_full * steady_odd
        even_calc = even_full * steady_even
        calculated = odd_calc + even_calc

        if(partial):
            # Add partial diagonals
            print("partial northwest",northwest[remainder+len(map)-2])
#            calculated += (full_gardens - 1) * (northwest[len(map)+remainder)]  )
#            exit()


        print("TODO... the long/med diags are going to vary now? Or not?")
            
        # undo:  changed these to -1 to account for index starting at 0
        # Add mid-steps
        calculated += full_gardens * (northwest[remainder+len(map)-2])
        calculated += full_gardens * (southwest[remainder+len(map)-2])
        calculated += full_gardens * (northeast[remainder+len(map)-2])
        calculated += full_gardens * (southeast[remainder+len(map)-2])

        # Add long steps
        calculated += (full_gardens+1) * (northwest[remainder-2])
        calculated += (full_gardens+1) * (southwest[remainder-2])
        calculated += (full_gardens+1) * (northeast[remainder-2])
        calculated += (full_gardens+1) * (southeast[remainder-2])


        print("TODO:  these indexes may be different now..")
        # print("plus one each of N,W,E,S at 'remainder' steps")
        orth_calc = steps-full_gardens*len(map)-int(ends[0]/2)-1
        calculated += north[orth_calc] + south[orth_calc] + east[orth_calc] + west[orth_calc]
        if(partial):
            calculated += north[len(map)+remainder-1] + south[len(map)+remainder-1] + east[len(map)+remainder-1] + west[len(map)+remainder-1]
        # print("plus one each of N,W,E,S at 'remainder' steps")

        if(remainder < 2):
            print("oops")
            exit()

        print("Calculated:",calculated)

        # this will not be equal in the test case due to the '14' edge.
        #print(west[remainder-1]+east[remainder-1]+steady_even*3+steady_odd*4)
#        print(north[orth_calc]+northwest[remainder-2]+northeast[remainder-2])
#        print(steady_even*1+steady_odd*0+northwest[remainder-2]+northeast[remainder-2]+northwest[remainder+len(map)-2]+northeast[remainder+len(map)-2])
#        print(west[remainder-1]+west[len(map)+remainder-1]+east[remainder-1]+east[len(map)+remainder-1]+steady_even*7+steady_odd*8)
#        print(steady_even*5+steady_odd*4+southwest[remainder-2]+southeast[remainder-2]+southwest[remainder+len(map)-2]+southeast[remainder+len(map)-2])
        #print(northwest[remainder+len(map)-2])
        print(steady_even)

        # okay right.. we changed the even/odd with test2

        #print("Oh, when the remainder is too small, the ends start filling out, with a non-full middle")
        # so all of the 'edge' fulls may not actually be full.

    # Alrighty, I need a 9x9 map to figure out where I'm going wrong.
    if(False):
        plots = copy.copy(cplots)
#        map = NineMap(map,plots)
        map = NineTeenMap(map,plots)

        Os = 0
        steps = 100
        for i in range(steps):
            plots = WalkThisWay(map,plots)


# TODO  Try calculation just one quadrant + middle
            

#        for y in range(len(map)):
        for y in range(22,33):
#            for x in range(len(map[y])):
            for x in range(99,110):
                if((y,x) in plots):
                    print("O",end='')
                    Os += 1
                else:
                    print(map[y][x],end='')
            print('')
        print("Actual:",len(plots))
        print("Os:",Os)

    # Find the steady state
    if(False):
        plots = {(0,0): 1} # start top left
        steps = 0
        prev_result = 0
        prev_prev_result = 0
        result = -1
        while(result != prev_prev_result):
            prev_prev_result = prev_result
            prev_result = result
            steps+=1
            print("Step:",steps)
            plots = WalkThisWay(map,plots)
            result = len(plots)
        
        print("Steady Steps:",steps-1)
        print("prev_prev_result:",prev_prev_result)
        print("prev_result:",prev_result)
        print("result:",result)


    if(False):
        steps = 130
        for s in range(steps):
            plots = WalkThisWay(map,plots)
        print(len(plots))


    if(False):
        for y in range(len(map)):
            for x in range(len(map[y])):
                if((y,x) in plots):
                    print("O",end='')
                else:
                    print(map[y][x],end='')
            print('')



