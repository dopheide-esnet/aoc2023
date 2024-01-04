#!/usr/bin/env python3

import pprint
import copy
import random
import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def BuildMesh(lines):
    mesh = dict()
    nodes = list()

    for line in lines:
        (src,dst) = line.split(":")
        if src not in mesh:
            mesh[src] = list()
        if(src not in nodes):
            nodes.append(src)
        dsts = dst.split(" ")
        dsts.remove('')
        for dst in dsts:
            if(dst not in nodes):
                nodes.append(dst)
            if(dst not in mesh[src]):
                mesh[src].append(dst)
            if(dst not in mesh):
                mesh[dst] = list()
            if(src not in mesh[dst]):
                mesh[dst].append(src)
    return (mesh,nodes)

def FindPath(a,b,mesh,path):

    current = list()
    path.append(a)

    if(len(path) > (100)):  # Bail on too long of path (educated guess)
                            # ..but, it'll keep trying these connections which suck.
                            # we need a 'bail' list for like the last 50 elements
                            # ugh, that doesn't work cause we might be real close to the right path in that last bit
        return current

    if(b in mesh[a]):
        path.append(b)
        current.append(path)
#        return current  # no need to go deeper
        return current

    for node in mesh[a]:
        if(node!=b):
            if(node not in path):
                possible = FindPath(node,b,mesh,copy.copy(path))
                for p in possible:
                    current.append(p)

    return current

def GetEdges(mesh):
    edges = list()
    for m in mesh:
        for n in mesh[m]:
            edge = m + "-" + n
            redge = n + "-" + m
            if(edge not in edges and redge not in edges):
                edges.append(edge)
    return edges

def RemainingEdges(mesh,original_mesh):
    remaining = list()
    for m in mesh:
        a = re.findall('...',m)
        b = re.findall('...',mesh[m][0])
        break
    # could look at the smallest list
    for n in a:
        for node in original_mesh[n]:
            if(node in b):
                remaining.append(n+node)
    return (remaining,len(a),len(b))

if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    # treat it like paths?
    # if there are more than 3 paths to get somewhere, that's not a link to disconnect... hhhmm

    (mesh,nodes) = BuildMesh(lines)
#    pprint.pprint(mesh)
#    print(len(nodes))


    # Implement Karger's Algorithm
    # https://en.wikipedia.org/wiki/Karger%27s_algorithm

    # Convert mesh to edge network?  # since we built that already
    pprint.pprint(mesh)

    original_mesh = copy.deepcopy(mesh)


    # BIG LOOP
    min = 0
    win = 0
    for x in range(1000):
        mesh = copy.deepcopy(original_mesh)
        print("Run:",x)

        while len(mesh) > 2:

            edges = GetEdges(mesh)
            random_edge = random.choice(edges)

            # TODO get rid of this 'edges' calculation from the loop
            # every edge should be represented in the 'mesh' dict twice.
            # would it be 'random' enough to select a random key and then a random thing from the list?

            


#            print(secrets.choice(edges))

            (a,b) = random_edge.split("-") # only works until we merge again and have a-b-c or a-b-c-d
            # combined again it could be ab-c though...
            c_list = []
            for n in mesh[a]:
                if(n != a and n != b and n not in c_list):
                    c_list.append(n)
            for n in mesh[b]:
                if(n != a and n != b and n not in c_list):
                    c_list.append(n)        
            mesh[a+b] = c_list
            del mesh[a]
            del mesh[b]
            for m in c_list:
                for i in range(len(mesh[m])):  # totally inefficient
                    if(mesh[m][i] == a):
                        mesh[m][i] = a+b
                    if(mesh[m][i] == b):
                        mesh[m][i] = a+b
                while(mesh[m].count(a+b) > 1):
                    mesh[m].remove(a+b) # if we had more than one.
                
#        pprint.pprint(mesh)
    #    pprint.pprint(original_mesh)

        (remaining,len_a,len_b) = RemainingEdges(mesh,original_mesh)
        print("Remaining:",len(remaining),remaining,len_a,len_b,len_a*len_b)
        if(len(remaining) < min or min==0):
            min=len(remaining)
            win=len_a*len_b
            if(min == 3):
                break

    print("Mininum:",min,win)

    # instead of keeping track of which links still remain at the end, we should be able to find
    # them by compairing with the original edge list.


    # stop when we get to len(mesh) == 2   Can we determine the number of edges connecting them?
    # what if we back up a step?



    exit()   # Throw away the rest of this for now.

    # We could keep a memory here.
    # If we're looking for A->C and we get to B and a known smallest exists from B->C, we can
    # skip the rest of the A->B->C calculation.

    # Can also cut off at length, it'll never be longer than the number of nodes
    # probably less than number of nodes / 2 or so.

    # TODO:  Keep track of the fastest path between any two nodes and continue
    # to back reference it.
    # Run through our list of nodes multiple times with different max lengths to help
    # build up the table.
    
    smallest = list()  # smallest paths between each set of nodes
    # LOOP OVER NODES?
    for i in range(len(nodes)):
        for j in range(i+1,len(nodes)):
            if(i != j):
                path = []
#    paths = FindPath('jqt','hfx',mesh,path)

                print("Finding path:",nodes[i],nodes[j])
                paths = FindPath(nodes[i],nodes[j],mesh,path)
#    pprint.pprint(paths)
                print(len(paths))
 
                small = len(paths[0])
                sp = paths[0]
                for p in paths:
                    if(len(p) < small):
                        small = len(p)
                        sp = p
                smallest.append(sp)

    print("Smallest paths",len(smallest))
#    pprint.pprint(smallest)

    # maybe, for each path, pick out 'links'.  like ntq<->jqt is a link.
    # count occurances.

    paths = smallest
    link_count = dict()
    for path in paths:
#        print("Path",path)
        for i in range(len(path)-1):
            link = path[i]+"-"+path[i+1]
            rlink = path[i+1]+"-"+path[i]
            if(link not in link_count and rlink not in link_count):
                link_count[link] = 1
            elif(link in link_count):
                link_count[link] += 1
            else:
                link_count[rlink] += 1

    print(dict(sorted(link_count.items(), key=lambda item: item[1])))
    # well that gives me 'pzl-hfx': 140, 'jqt-nvd': 182} as standouts, but not the other.
    # not enough of a pattern to go off of.
    # what if we calculated all of the shortest paths...





