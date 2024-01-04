#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

# ??
class Map():
    def __init__(self,dst):
        self.dst = dst
        self.rows = list()

def GetMaps(lines):
    maps = dict()
    seeds = list()

    # try indexing maps by source type
    sline = lines.pop(0)
    (s,n) = sline.split(":")
    seeds = n.split(" ")
    seeds = [int(i) for i in seeds if i]

    data = False
    for line in lines:
        if(not data):
            m = re.search(r'^(\w+)-to-(\w+) map',line)
            if(m):
                src = m.group(1)
                dst = m.group(2)
                data = True
                maps[src] = Map(dst)
        else:
            if line == '':
                data = False
            else:
                (dst_s,src_s,r) = line.split(" ")
                dst_s = int(dst_s)
                src_s = int(src_s)
                r = int(r)
                maps[src].rows.append((dst_s,src_s,r))

    return (seeds,maps)

def PrintMaps(maps):
    for map in maps:
        print(f"{map} to {maps[map].dst}")
        for row in maps[map].rows:
            print(row)

def GetSeedLocation(seed,maps):
    item = seed
    src = "seed"
    end = "location"
    while(end != "done"):
#        print(f"Item: {item} ")
#        print(f"From {src} to {maps[src].dst}")
        for (dst_s,src_s,r) in maps[src].rows:
            if(item >= src_s and item < (src_s + r)):
                # item is within this src range, get the next item
                diff = item - src_s
#                print("diff",diff)
                item = dst_s + diff
#                print(f" to {maps[src].dst}: {item}")
                break

        if(maps[src].dst == end):
            end = "done"
        src = maps[src].dst  # update to the next source map

    return item     


if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    (seeds,maps) = GetMaps(lines)
#    PrintMaps(maps)

    min = 0
#    for seed in seeds:
#        loc = GetSeedLocation(seed,maps)
#        if(min == 0):
#            min = loc
#        elif(loc < min):
#            min = loc
#    print("Part 1:",min)
    
    i = 0
    while i < len(seeds):
        print("Processing range", i)
        for seed in range(seeds[i],(seeds[i]+seeds[i+1])):

            loc = GetSeedLocation(seed,maps)
            if(min == 0):
                min = loc
            elif(loc < min):
                min = loc

        i += 2
    print("Part 2:",min)

