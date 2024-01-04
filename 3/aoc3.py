#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

class Schematic:
    def __init__(self,val):
        self.is_num = False  # or symbon
        self.coords = list()
        self.val = val
        self.adj_list = list()

def PrintSchematic(data):
    for d in data:
        print(f"{d}: {data[d].val} {data[d].is_num} {data[d].coords}")
        if(len(data[d].adj_list) > 0):
            print(data[d].adj_list)

def BuildData(lines):
    data = dict()
    for y in range(len(lines)):
        row = list(lines[y])
        for x in range(len(row)):
            if(row[x] == '.'):
                continue
            if(row[x].isdigit()):
                if(x > 0 and (y,x-1) in data and data[(y,x-1)].is_num):
                        # if previous spot is a number. update 'end' coord dict key, coords, and val
                        data[(y,x)] = data[(y,x-1)]
                        data[(y,x)].coords.append((y,x))
                        data[(y,x)].val += row[x]
                        del data[y,x-1]
                else:
                    sch = Schematic(row[x])
                    sch.coords = [(y,x)]
                    sch.is_num = True
                    data[(y,x)] = sch
            else:
                sch = Schematic(row[x])
                sch.coords = [(y,x)]
                data[(y,x)] = sch

    # When we're done, go back and update 'val's to int(val)?
    for blaa in data:
        if(data[blaa].is_num):
            data[blaa].val = int(data[blaa].val)

    return data

def GetSymbolCoords(data):
    symbols = list()
    for d in data:
        if not data[d].is_num:
            symbols.append(d)
    return symbols

def CheckAdj(c,symbols):
    (y,x) = c
    c_list = [(y-1,x-1),(y-1,x),(y-1,x+1),(y,x-1),(y,x+1),(y+1,x-1),(y+1,x),(y+1,x+1)]
    for c_test in c_list:
        if(c_test in symbols):
            return True

    return False

def UpdateSymAdj(sym,data):
    (y,x) = sym
    c_list = [(y-1,x-1),(y-1,x),(y-1,x+1),(y,x-1),(y,x+1),(y+1,x-1),(y+1,x),(y+1,x+1)]

    for d in data:
        if(data[d].is_num):
            for c in data[d].coords:
                if(c in c_list):
                    data[sym].adj_list.append(data[d].val)
#                    print(f"{data[sym].val} is adj to {data[d].val}")
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

    data = BuildData(lines)
    symbols = GetSymbolCoords(data)

    total = 0
    for d in data:
        # Part 1
        if(data[d].is_num):
            # for each coord, check adjaceny
            for c in data[d].coords:
                if(CheckAdj(c,symbols)):
                    total += data[d].val
                    break

        # Part 2
        else:
            if(data[d].val == "*"):
                UpdateSymAdj(d,data)

    print("Part 1:", total)

#    PrintSchematic(data)
    total = 0
    for d in data:
        if len(data[d].adj_list) == 2:
            power = data[d].adj_list[0] * data[d].adj_list[1]
            total += power
    print("Total:",total)
