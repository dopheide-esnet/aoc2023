#!/usr/bin/env python3

import copy

testcase = True
if testcase:
    file = "test2.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def ParseLines(lines):
    all_springs = list()
    for line in lines:
        (s,c) = line.split(" ")
        springs = list(s)
        counts = c.split(",")
        counts = [int(i) for i in counts if i]
        all_springs.append((springs,counts))
    return all_springs


def Poss2(s,springs,c,counts):

    finish = False
    poss_return = list()

    if(s >= len(springs)):
#        print("Too far")
        return list()

    # skip dividers
#    print(len(springs),s)
    while(springs[s] == "."):
        if(s == len(springs) - 1):
            break
        s += 1


    if(counts[c] > len(springs) - 1):
#        print("Not enough room to finish, fail")
        return list()
        # TODO, do something

    # Try doing skips before placement, maybe it'll be easier to add them up.

    # if that works or fails, try skipping, keeping c the same
    new_s = s
    known = springs[s:].count("#")
    needed = sum(counts[c:])
    known_dots = springs[s:].count(".")

    needed_dots = len(counts[c:]) - known_dots
#    print("len counts",len(counts[c:]))
#    print("Known, Needed",known,needed)
#    print("dots",needed_dots)
    while(springs[new_s] != "#"):  # can't skip a #
        new_s += 1
#        print("new len",len(springs[new_s:]))


### TODO... ALSO SUBTRACT NUMBER OF KNOWN '.'S
### made it slower?

        if(len(springs[new_s:]) < (needed - known - needed_dots)):  # could add needed '.'s into this math?
#            print("No room")
            break
#        print("skip and go to",new_s)
        new_springs = copy.copy(springs)
        check = Poss2(new_s,new_springs,c,counts)
        if(len(check) == 0):
            break
        else:
            poss_return.extend(check)

#    print("Try placing original and going to next c")
    
    # try placing it.
    yes = True
    for i in range(counts[c]):  # check if it fits.
        if(len(springs) > s+i):
#        if(s+i < len(springs)):
            if(springs[s+i] == "."):
#            print("It can't go here",s+i, "poss",poss_return)  # skip one
                yes = False
                break

    if(yes):  # length check
        if(s+counts[c] < len(springs)):
            if(springs[s+counts[c]] == "#"):  # would be too long a spring
#                print("Too long")
                yes = False
        if(s+counts[c] > len(springs)):  # NEW THING
           yes = False

    if(yes):
#        print("Place it",s,c)
#        print(len(springs),s,counts[c])
        for i in range(counts[c]):
            springs[s+i] = "#"
        
        # sanity check
        if(springs.count("#") > sum(counts)):
            # NOPE, fuck off!
            return poss_return
        if(c < len(counts) - 1):
            new_springs = copy.copy(springs)
#            print("Go to next c at",s+counts[c]+1)
            # must skip s+counts[c] so we have a divider
            check = Poss2(s + counts[c] + 1,new_springs,c + 1,counts)
            if(len(check) != 0):
               # yes = False
                poss_return.extend(check)
        else:
#            print("That was the end")
            poss_return.append(springs)
            finish = True

    # else:  return 0  

    # need to return list of spring possibilities.
    # must be complete and UNIQUE

#    print("Returning:",poss_return,c)
    return poss_return


def DoBetter(prev,s,springs,c,counts):
    options = 0
    both = False
    failed = False

    results = 0
    l_results = 0
    r_results = 0
    print("At",s,c)
    if(springs[s] == "?"):
        both = True

        # TODO:  Don't bother doing both if this is the last spot
        # could also throw off count

    if(springs[s] == "." or both):
        # There's only one option here, skip
        if(not both):
            print("skip solo .")
        else:
            print("skip fake .")
        l_results = DoBetter(".",s+1,springs,c,counts)
        if(l_results > 0):
            options += 1
    if(springs[s] == "#" or both):
        print("going #")
        # will the next c fit?
        num = s+counts[c]
        if(prev=="#"):
            print("Failed prev check")
            failed = True
        # not enough room
        #### NUM >= is wrong also
        if(c < len(counts)-1 and num >= len(springs) and not failed):  #???
            print("Failed room check")
            failed = True
        # there is a divider in the way or a # after it.
        if(not failed):
            if(springs[s:num].count(".") > 0):
                print("Failed . check")
                failed = True
        print(len(springs),num)
        if(not failed):
            if(c < len(counts)-1 and springs[num] == "#" and not failed):
                print("Failed next # after check")
                failed = True
        if(not failed):
            print("Need to check if this is the last one and just return??")
            # if it's the last c and there are no more '#'s left in springs..
            if(c+1 == len(counts)):
                if(springs[num:].count("#") > 0):
                    print("ended too soon")
                    failed = True
                else:
#                    results = 1
#                    options += 1
                    print("SUCCESS, just return 1?")
                    
                    return 1
            else:
                r_results = DoBetter("#",num,springs,c+1,counts)  # ?? this should be just 'num' ?
                if(r_results > 0 ):
                    options += 1

    print("Returning from",s,c,l_results,r_results,options,"     ",(l_results + r_results) * options)
    results = l_results + r_results  # ???
    return (results * options)


if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    all_springs = ParseLines(lines)

    for (springs,counts) in all_springs:
        print(springs,counts)
        count = DoBetter("",0,springs,0,counts)
        print("Count",count)
#        exit()


    print("Need Part2 multiples")
    exit()
    # Shitty Part1 below
    total = 0
    working_on = 1
    for (springs,counts) in all_springs:
#        print(working_on)
        working_on += 1
        ## PART 2 NONSENSE
#        extra = copy.copy(springs)
#        cextra = copy.copy(counts)
#        for i in range(4):
#            springs.append("?")
#            springs.extend(extra)
#            counts.extend(cextra)

#        print("".join(springs),counts)
        check = Poss2(0,springs,0,counts)
        for t in range(len(check)):
            for s in range(len(check[t])):
                if(check[t][s] == "?"):
                    check[t][s] = "."
        unique_data = [list(x) for x in set(tuple(x) for x in check)]
#        print(len(unique_data))
#        for u in unique_data:
#            print("".join(u))
        total += len(unique_data)

    print("Part 1:",total)
