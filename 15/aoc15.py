#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def Hash(ins):
    count = 0
    chars = list(ins)
    for c in chars:
        count += ord(c)
        count *= 17
        count = count % 256
    return count

def AddtoBox(hash,label,focal,boxes):
#    boxes[hash][0] = list of labels in order  (so we can use 'blaa' in list, list.index)
#    boxes[hash][1] = dict of labels w/ focal length

    if(hash not in boxes):
        boxes[hash] = list()
        boxes[hash].append(list())
        boxes[hash].append(dict())
    if(label not in boxes[hash][0]):
        boxes[hash][0].append(label)
        boxes[hash][1][label] = focal
    else:
        # we don't move the label in the list, just update it's focal length in the dict
        boxes[hash][1][label] = focal

def RemovefromBox(hash,label,boxes):
    if(hash not in boxes):
        return
    if(label not in boxes[hash][0]):
        return
    boxes[hash][0].remove(label)

def PrintBoxes(boxes):
    for b in boxes:
        print(f"Box {b}: ",end='')
        for i in range(len(boxes[b][0])):
            print(f"{boxes[b][0][i]} {boxes[b][1][boxes[b][0][i]]} ")

if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    instructions = lines[0].split(",")

    total = 0
    boxes = dict()
    for ins in instructions:
        if('=' in ins):
            (label,focal) = ins.split("=")
            focal = int(focal)
            hash = Hash(label)
            AddtoBox(hash,label,focal,boxes)            
        else:
            (label,trash) = ins.split("-")
            hash = Hash(label)
            RemovefromBox(hash,label,boxes)

        total += Hash(ins)

    print("Part1:",total)

#    PrintBoxes(boxes)

    # calculate power
    total = 0
    for b in boxes:
        for i in range(len(boxes[b][0])):
            label = boxes[b][0][i]
            power = ( b+1 ) * (i+1) * (boxes[b][1][label])

#            print(b,i,label,"Power:",power)
            total += power
    print("Part2:",total)
#hash on the label



