#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def GrabInput(lines):
    seqs = list()
    for line in lines:
        nums = line.split(" ")
        nums = [int(i) for i in nums if i]
        seqs.append(nums)
    return seqs

def GetNext(seq):
    # Brute force it for Part 1 because we don't know what they want in Part 2
    # but I think we can start from the back end for efficiency and not have to 
    # calculate the whole pyramid.
    new_seq = list()
    for i in range(len(seq)-1):
        new_seq.append(seq[i+1]-seq[i])
    if(len(new_seq) > 1 and (new_seq[-2] == 0 and new_seq[-1] == 0)): # last two are 0, we're done.
        return 0
    elif(len(new_seq) == 1) and new_seq[0] == 0:
        return 0
    else:
        add = GetNext(new_seq)

    return new_seq[-1] + add

def CheckZero(seq):
    for s in seq:
        if(s != 0):
            return False
    return True

def GetPrev(seq):
    new_seq = list()
    for i in range(len(seq)-1):
        new_seq.append(seq[i+1]-seq[i])

    if(CheckZero(new_seq)):
        return 0
    else:
        sub = GetPrev(new_seq)

    print(new_seq, new_seq[0]-sub)
    return new_seq[0] - sub 

if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    sequences = GrabInput(lines)

#    total = 0
#    for seq in sequences:
#        add = GetNext(seq)
#        new = seq[-1]+add
#        seq.append(new)
#        total += new
#    print("Part 1:",total)
    total = 0
    for seq in sequences:
        print(seq)
        sub = GetPrev(seq)
        new = seq[0]-sub
        print(new)
        total += new
    print(total)


