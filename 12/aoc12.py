#!/usr/bin/env python3

import copy

cache = dict()

testcase = False
if testcase:
    file = "test.txt"
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


def DoBetter(s,springs,c,counts):
    ''' Start at the end '''
    options = 0
 
    print("At",s,c)

    # check if this is a known '.' and just back up?
    while(springs[s] == '.' and s > 0):
        s -= 1

    # would the spring fit here.
    proceed = False
    must_proceed = False # if any s in range[counts[c]] == #, we HAVE to place a spring here
    while(not proceed and s-counts[c] >= -1):
        proceed = True
        for i in range(counts[c]):
            # it can't fit here, back up and try again.
            if(springs[s-i] == '.'):
                proceed = False
                s -= 1
            elif(springs[s-1] == "#"):
                must_proceed == True
        if(must_proceed):
            break

#    if not proceed:
#        print("Return dead end")
#        return 

    # Need to check that s+1 isn't a # (must be a space between springs)
    if(s < len(springs)-1):
        if(springs[s+1] == "#" and must_proceed):
            # wha hwa.
            print("Dead end 3")
            proceed = False
#            return 
    
        if(springs[s+1] == "#"):
            proceed=False

    if(proceed):
        print("Proceed here",s,c)
        options += 1

    # TODO if this is a '?' we also process s-1, if length and .count() of # and ? are enough.
    if(springs[s] == '?'):
        print("We can optionally back up")
        print("Assuming remaining space would be enough.")
        available = springs[0:s].count('#') + springs[0:s].count('?')
        needed = sum(counts[:c+1])

        # This could also include the number of needed spaces between springs.
        # so..  needed += len(counts[:c+1]-1  ?  but we didn't count available spaces

        # If things break, check here.
        if(needed > available):
            print("Dead end 2, also no reason to go backwards")
            return 0 # ?
        else:
            print("Proceed at s-1 with c",s-1,c)
            result = DoBetter(s - 1, springs, c, counts)
            print("Return from s-1 with c",s-1,c)


    # planned backup for next springs in counts
    if(c > 0):
        print("Proceed at s-1 with c-1") 
        # if we can proceed.. set new s and new c.
        result = DoBetter(s - counts[c], springs, c - 1, counts)

    # check if we make this a '.', is there still enough previous room for the counts
    # track via cache?

    return 


def DoBetter2(s,springs,c,counts):
    ''' Start at the front '''
    global cache
    options = 0
 
#    print("At",s,c)
    # TODO:  Check cache
#    if((s,c) in cache):
#        print("Cache return",s,c)
#        return cache[(s,c)]

    if(s == len(springs)):
#        print("EOL")
        return 0

    # check if this is a known '.' and just move forward
    while(springs[s] == '.' and s < len(springs)-1):
        s += 1

#    if(s == len(springs)):
#        print("EOL")
#        return 0

    available = springs[s:].count('#') + springs[s:].count('?')
    needed = sum(counts[c:])
    if(needed > available):
 #       print("No space")
        return 0

    # check if current space is #, then must_proceed
    if(springs[s] == "#"):
#        print("must proceed")
        if(springs[s:s+counts[c]].count(".") > 0):
#            print("Ran into a space")
            return 0

    must_skip=False
    if(s+counts[c] < len(springs)):
        if(springs[s+counts[c]] == "#"):
#            print("Ran into a spring",s,c)
            # so we can't put it here, but we could skip it.
            must_skip=True
#            return 0

    # put it here and proceed down s+counts[c]+1?, c+1
    # populating cache the whole way

    if(not must_skip):
        if(c == len(counts)-1):  # last count
#            print("last count",s,c)
#            print(s+counts[c],len(springs)-1)
            
            if(s + counts[c] < len(springs)-1 and springs[s+counts[c]:].count("#") > 0):

                # there's still a chance?
                if(springs[s] == '?'):
                    must_skip = True # ?
                else:
                    return 0

            else:
                # ?.??#????? is not and end
                if(springs[s:s+counts[c]].count(".") == 0):
                    options += 1
#                    print("end here")
                    # _AN_ end, doesn't mean the only end.  Could still skip
                must_skip=True

        # Check for space for just this count[c] at s
        if(springs[s:s+counts[c]].count(".") > 0):
#            print("Ran into a space here")
            must_skip=True


        if(not must_skip):

            ### THIS IS WHERE WE INCORRECTLY ASSUMED IT GOT PLACED
            new_s = s+counts[c]+1
            new_c = c+1

            if((new_s,new_c) in cache):
#                print("Cache return (2)",new_s,new_c)
                result = cache[(new_s,new_c)]
            else:
                result = DoBetter2(new_s,springs,new_c,counts)
                cache[(new_s,new_c)] = result
#                print("save to cache ",new_s,new_c,result)
            
            options += result

    # CACHE if result?
    # TODO  SAVE TO CACHE, no, can't save until we get a return from an 'end'
    # but can then save all the way back.


    if(springs[s] == '?' and s < len(springs)):   # < len(springs) - 1 ?
#        print("skip")
        # this is what gives us options += 1 ?

        new_s = s+1
        new_c = c

        if((new_s,new_c) in cache):
#            print("Cache return (3)",new_s,new_c)
            result = cache[(new_s,new_c)]
        else:
            result = DoBetter2(new_s,springs,new_c,counts)
            cache[(new_s,new_c)] = result
#            print("save to cache (2)",new_s,new_c,result)

        options += result

    # CACHE and save to cache here? if result?

    return options


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
#    print(all_springs)

#    i = 1
#    for (springs,counts) in all_springs:
#        print(i,springs,counts)
#        count = DoBetter("",0,springs,0,counts)
#        print("Count",count)
#        i += 1
#        exit()

    total = 0
    working_on = 1
    for (springs,counts) in all_springs:
#        print("Line:",working_on)

        ## Do first part only
#        check = DoBetter2(0,springs,0,counts)

        # Do Part 2
        extra = copy.copy(springs)
        cextra = copy.copy(counts)

        for i in range(4):
            springs.append("?")
            springs.extend(extra)
            counts.extend(cextra)

        check = DoBetter2(0,springs,0,counts)


        # clear cache
        cache = dict()
        total += check
        working_on += 1

    print("Total:",total)
    exit()

    if(False):
        # Shitty partial Part2 attempt below
        total = 0
        working_on = 1
        for (springs,counts) in all_springs:
            print(working_on)
            working_on += 1

            osprings = copy.copy(springs)
            ocounts = copy.copy(counts)
            oosprings = copy.copy(springs)
            oocounts = copy.copy(counts)

            ## Do first phase
            check = Poss2(0,springs,0,counts)
            for t in range(len(check)):
                for s in range(len(check[t])):
                    if(check[t][s] == "?"):
                        check[t][s] = "."
            unique_data = [list(x) for x in set(tuple(x) for x in check)]
            step1 = len(unique_data)

            ## PART 2 NONSENSE
            extra = copy.copy(osprings)
            cextra = copy.copy(ocounts)

            for i in range(1):
                osprings.append("?")
                osprings.extend(extra)
                ocounts.extend(cextra)

    #        print("".join(springs),counts)

            check = Poss2(0,osprings,0,ocounts)
            for t in range(len(check)):
                for s in range(len(check[t])):
                    if(check[t][s] == "?"):
                        check[t][s] = "."
            unique_data = [list(x) for x in set(tuple(x) for x in check)]
    
            step2 = len(unique_data)



    #        for u in unique_data:
    #            print("".join(u))
            total += step1 * (multiplier)**4

        print("Part 1:",total)

    # Shitty Part1 below
    total = 0
    working_on = 1
    for (springs,counts) in all_springs:
#        print(working_on)
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
#        print("Line:",working_on,"Result:",len(unique_data))
        total += len(unique_data)
        working_on += 1

    print("Part 1:",total)