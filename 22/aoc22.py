#!/usr/bin/env python3

import copy
import sys

sys.setrecursionlimit(2000)

maxh = 0
maxz = -1
testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

class Block:
    def __init__(self,id,start,stop):
        self.id = id
        self.start = start
        self.stop = stop
        self.blocks = self.Calc(start,stop)
        self.supporter = list()    # list of block ids
        self.supported = list()  # list of block ids
        self.mz = -1
        self.d_list = {}
        self.reaction = False
#        self.minz = 0  # calculated later
    def Calc(self,start,stop):
        blocks = []
        blocks.append(start)
        (sx,sy,sz) = start
        (zx,zy,zz) = stop
# this shouldn't matter ?
#        if(sx == zx and sy == zy and sz == zz):
#            print("Single")
#            exit()
        if(zx < sx or zy < sy or zz < sz):
            print("backwards")
            exit()
        if(sx != zx):
            for x in range(zx-sx-1):
                blocks.append((sx+x+1,sy,sz))
        elif(sy != zy):
            for y in range(zy-sy-1):
                blocks.append((sx,sy+y+1,sz))
        elif(sz != zz):
            for z in range(zz-sz-1):
                blocks.append((sx,sy,sz+z+1))        
        blocks.append(stop)
        return blocks
    def __lt__(self,other):
        (sx,sy,sz) = self.start
        (ox,oy,oz) = other.start
        return sz < oz

def fast_forward(i,blocks):
    global maxz
    # Fast Forward
    # what is our minimum z?
    (x,y,minz) = blocks[i].start
    for b in blocks[i].blocks:
        (x,y,z) = b
        if(z < minz):
            minz = z
    if(minz > maxz + 1 ):
        diff = minz - (maxz + 1)
        for j in range(len(blocks[i].blocks)):
            (x,y,z) = blocks[i].blocks[j]
            z -= diff
            blocks[i].blocks[j]=(x,y,z)
        minz -= diff
    blocks[i].minz = minz


def drop_ghost(ghost):
    for i in range(len(ghost)):
        (x,y,z) = ghost[i]
        ghost[i] = (x,y,z-1)
    return ghost

def this_is_your_downfall(i,blocks):
    global maxz
    '''
    block falls down..  fast forward to global max Z
    check...  decrease all of its 'blocks' Z's by 1.
    compare to all blocks below it that have a maxz of z

    if no interference, step down

    else... make sure we have all supporting blocks at thatlevel.
    populate supprting and supported.  set maxz
    '''
#    print(blocks[i].id,blocks[i].start,blocks[i].stop,blocks[i].blocks)

#    print("Dropping Block:",blocks[i].id)

    fast_forward(i,blocks)
#    print("FF:",blocks[i].blocks,blocks[i].minz)

    # k, so for all blocks under this one that have a mz == maxz we need to check
    # for interference

    settled = False
    # to make comparisons easier, we'll make a ghost block
    ghost = copy.copy(blocks[i].blocks)
    ghostz = maxz + 1

    while(not settled):
        ghost = drop_ghost(ghost)
        ghostz -= 1

        if(ghostz == 0):
#            print("Ground")
            for g in range(len(blocks[i].blocks)):
                (x,y,z) = blocks[i].blocks[g]
                if(z > blocks[i].mz):
                    blocks[i].mz = z
            return

        for k in range(i):  # for all blocks under this one
            if(blocks[k].mz == ghostz):
                for gb in ghost:
                    if(gb in blocks[k].blocks):
#                        print("ghost Interference!!!",gb)
                        if(i not in blocks[k].supporter):
                            blocks[k].supporter.append(i)
                        if(k not in blocks[i].supported):
                            blocks[i].supported.append(k)
                        # drop block
                        # block is at maxz + 1 right now.
                        # could skip the decrease part of the loop, but need to set new mz anyway
    #                    if(ghostz != maxz):
                            # no block change
                        if(not settled):
                            diff = maxz - ghostz
                            new_mz = 0
                            for j in range(len(blocks[i].blocks)):
                                (x,y,z) = blocks[i].blocks[j]
                                z -= diff
                                if(z > new_mz):
                                    new_mz = z
                                blocks[i].blocks[j] = (x,y,z)
                            blocks[i].mz = new_mz

                                # ghostz + 1 will be our level
                            if ghostz + 1 > maxz:
                                maxz = ghostz + 1
                        settled = True
                        # mark as supporter and supported by, but keep looking for more at this level
                        # also drop active block to ghostz + 1
                        # set active block's mz.  Raise global maxz if necessary
                        # settled = True

    return




def Reaction(next_group,blocks):
    ng=list()

    for n in next_group:
        if(len(blocks[n].supported) == 1):
            p = blocks[n].supported[0]
            blocks[p].d_list[n] = "True"
            blocks[p].d_list = blocks[p].d_list | blocks[n].d_list  # merge the d_list down
            blocks[n].reaction=True
#            print(p,blocks[p].d_list)
            ng.append(p)

    return ng



def TryReaction(i,blocks,proposed,height):
    global maxh

    if(i not in proposed[height]):
        print("wtf")
        exit()

    proposed[height][i] = True  # we're doing this one, don't need to do it again.
#    print(i,"at height",height,maxh)

#    if(len(blocks[i].supporter)) == 0:
        # end block
#        return 0

    for s in blocks[i].supporter:

        will_fall = True
        for sb in blocks[s].supported:
            if(sb not in proposed[height]):
                will_fall = False

            # debugging sanity check
                for hh in proposed:
                    if sb in proposed[hh]:
                        print("wtf2")
                        exit()



        if(will_fall):
#            print("  ",s,"will fall")
            new_height = blocks[s].mz
            if(new_height > maxh):
                maxh = new_height
            if(new_height not in proposed):
                proposed[new_height] = dict()
            proposed[new_height][s] = False

#    print("New Proposed,",proposed)

    # continue processing this height before moving on.
    go_big = True
    for p in proposed[height]:
        if(proposed[height][p] == False):
            go_big = False
            TryReaction(p,blocks,proposed,height)
            break        

    if(go_big):
        # next available height in proposed
        height += 1
#        print("New Height",height)
        while(height <= maxh):
            if(height in proposed):
                break
            height+=1

        # could just grab index 0?  
        if(height in proposed):
            for p in proposed[height]:
                if(proposed[height][p] == False):
                    TryReaction(p,blocks,proposed,height)
                    break



if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    blocks = list()
    for i in range(len(lines)):
        (start,stop) = lines[i].split("~")
        (x,y,z) = start.split(",")
        x = int(x)
        y = int(y)
        z = int(z)
        start = (x,y,z)
        (x,y,z) = stop.split(",")
        x = int(x)
        y = int(y)
        z = int(z)
        stop = (x,y,z)        
        blocks.append(Block(i,start,stop))

    # what.. they did give the start blocks in order...
    blocks.sort()
    for b in blocks[0].blocks:
        (x,y,z) = b
        if z > maxz:
            maxz = z
    blocks[0].mz = maxz

    stop = 10
    for i in range(1,len(blocks)):
#    for i in range(1,10):
        this_is_your_downfall(i,blocks)

#    g = 0
    for b in range(len(blocks)):
#        g+=1
#        if(g==stop):
#            exit()
        print(b,blocks[b].supported,blocks[b].supporter)
    
    # Can Disintegrate?
    not_blow_up = dict()
    for b in blocks:
        if(len(b.supporter) == 0):
            not_blow_up[b.id] = True
        elif(len(b.supported) == 1):
            not_blow_up[b.supported[0]] = True
    print("Part 1",len(blocks)-len(not_blow_up))

    total = 0
    for i in range(len(blocks)):
        proposed = dict()  # dict[height] of dict
        proposed[blocks[i].mz] = dict()
        proposed[blocks[i].mz][i] = False
        maxh = blocks[i].mz
        result = TryReaction(i,blocks,proposed,blocks[i].mz)    
        # count True's?
        count = 0
        for h in proposed:
            for p in proposed[h]:
                if proposed[h][p] == True:
                    count += 1
        print("Count",i,count-1)
        total += count - 1
    print("Part2:",total)
