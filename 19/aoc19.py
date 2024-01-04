#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

class Workflow:
    def __init__(self,name,tests):
        self.name = name  # probably also a dict key
        self.tests = tests  # can we use 'eval()' for the tests?

class Part:
    def __init__(self,x,m,a,s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

class Option:
    def __init__(self):
        self.xmin = 1
        self.xmax = 4000
        self.mmin = 1
        self.mmax = 4000
        self.amin = 1
        self.amax = 4000
        self.smin = 1
        self.smax = 4000

def ParseLines(lines):
    workflows = dict()
    parts = list()
    parts_parse = False

    workflow_re = re.compile(r'^(\w+)\{(.*)\}$')
    parts_re = re.compile(r'^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}')

    for line in lines:
        if line == "":
            parts_parse = True
            continue
        if not parts_parse:
            m = workflow_re.search(line)
            if(m):
                name = m.group(1)
                tests = m.group(2)
                tests = tests.split(",")
            workflows[name] = Workflow(name,tests)
        else:
            p = parts_re.search(line)
            if(p):
                x = int(p.group(1))
                m = int(p.group(2))
                a = int(p.group(3))
                s = int(p.group(4))
            parts.append(Part(x,m,a,s))  

    return (workflows,parts)

def ProcessPart(part,workflows,wf):
    dest = "none"

    for test in workflows[wf].tests:
        if(":" in test):
            (condition,dest) = test.split(":")
            blaa = "part." + condition
            if(eval(blaa)):
#                print("new dest",dest)
                break
            else:
                continue # to next test
        else:
            dest = test
#            print("no conditional",dest)
    if(dest == "none"):
        print("oops")
        exit()

    if(dest == 'A'):
        return True
    elif(dest == 'R'):
        return False
    else:
        return ProcessPart(part,workflows,dest)

def GetCombos(combos,workflows,wf):

    stuff = ""
    for test in workflows[wf].tests:
        if(":" in test):
            (condition,dest) = test.split(":")
            combos[stuff + " " + condition] = dict()

            # need to check dest if R or A here.
            if(dest == "R"):
                combos[stuff + " " + condition] = "R"
            elif(dest == "A"):
                combos[stuff + " " + condition] = "A"
            else: 
                GetCombos(combos[stuff + " " + condition],workflows,dest)

            stuff = "not " + condition
            continue
        else:
            if(test == "R"):
                stuff = stuff + " R"
                combos[stuff] = "R"
            elif(test == "A"):
                stuff = stuff + " A"
                combos[stuff] = "A"
            else:
                # it's just a new workflow destination
                combos[stuff] = dict()
                GetCombos(combos[stuff],workflows,test)

def UpdateOptions(negate,c,result):
    m = re.search(r'^\s?(\w)([\<\>])(\d+)\s?$',c)
    if(m):
        var = m.group(1)
        op = m.group(2)
        val = int(m.group(3))
    else:
        print("oops")
        exit()

    if(op == "<"):
        if(var == 's'):
            if(not negate and result.smax > val - 1):
                result.smax = val - 1
            elif(negate and result.smin < val):
                result.smin = val
        if(var == 'x'):
            if(not negate and result.xmax > val - 1):
                result.xmax = val - 1
            elif(negate and result.xmin < val):
                result.xmin = val    
        if(var == 'a'):
            if(not negate and result.amax > val - 1):
                result.amax = val - 1
            elif(negate and result.amin < val):
                result.amin = val
        if(var == 'm'):
            if(not negate and result.mmax > val - 1):
                result.mmax = val - 1
            elif(negate and result.mmin < val):
                result.mmin = val

    if(op == ">"):
        if(var == 's'):
            if(not negate and result.smin < val + 1):
                result.smin = val + 1
            elif(negate and result.smax > val):
                result.smax = val
        if(var == 'x'):
            if(not negate and result.xmin < val + 1):
                result.xmin = val + 1
            elif(negate and result.xmax > val):
                result.xmax = val
        if(var == 'm'):
            if(not negate and result.mmin < val + 1):
                result.mmin = val + 1
            elif(negate and result.mmax > val):
                result.mmax = val
        if(var == 'a'):
            if(not negate and result.amin < val + 1):
                result.amin = val + 1
            elif(negate and result.amax > val):
                result.amax = val
    return result

def DoMathOrig(combos):

### turn all this shit into a list?
# how to deal with lots of < and > for a single variable
    this_layer = list()

    print("start",len(combos))
    for c in combos:
        result = list()
        if(not isinstance(combos[c],str)):
            result = DoMath(combos[c])
            if(not len(result) == 1):
                print("todo, multiple options in list")
                exit()
            if result[0]=='R':
                continue
            elif result[0]=='A':
                # don't just add it, but return a set of variable extents?
                return [Option()]
            else:
                # the result should be an Option()
                # TODO, or list of options??

                m = re.search(r'^\s?(\w)([\<\>])(\d+)\s?$',c)
                if(m):
                    var = m.group(1)
                    op = m.group(2)
                    val = int(m.group(3))
                    result[0] = UpdateOptions(False,result[0],var,op,val)
                    print(result[0].smin,result[0].smax)

                else:
                    n = re.search(r'^\s?not\s(\w)([\<\>])(\d+)\s?$',c)
                    if(n):
                        var = n.group(1)
                        op = n.group(2)
                        val = int(n.group(3))
                        print("not",var,op,val)
                        result[0] = UpdateOptions(True,result[0],var,op,val)
                        print(result[0].smin,result[0].smax)

                    else:
                        ### TODO, 'c' may also be multiple things divided by spaces?
                        print("Match failed on",c)
                        exit()

        else:
            print(combos[c])
            if(combos[c] == 'A'):
                print("Return A")
                return ["A"]
            else:
                return ["R"]  # to be dropped
            # if it's R, it's not an option.
            # if it's A, return as a new list item

        print("Done with",c,"append to this_layer")
        this_layer.extend(result)
    
    print("returning",len(this_layer))
    return this_layer

def DoMath(workflows,wf):
    print("Doing wf",wf)

    this_layer = list()
    negative_mods = list()

    for test in workflows[wf].tests:

        if(":" in test):
            (condition,dest) = test.split(":")
            print(wf,"hit a real condition",condition)

            if(dest == 'A'):
                print(wf,"condition resutls in A")
                result = [Option()]
                result[0] = UpdateOptions(False,condition,result[0])
                # mod options, plus any negatives
                for n_cond in negative_mods:
                    result[0] = UpdateOptions(True,n_cond,result[0])
                print(wf,result[0].xmin,result[0].xmax)
                this_layer.append(result[0])
                # add to this_layer
            elif(dest == 'R'):
                print("condition results in R")  # so it doesn't get added
                # Not sure this is totally right, should we somehow remove previous results that called this?
            else:
                # dest is a real dest and condition is true
                result = DoMath(workflows,dest)
                if(len(result) > 0):
                    for r in range(len(result)):
                        print("mod options for",result[r])
                        result[r] = UpdateOptions(False,condition,result[r])
                        for n_cond in negative_mods:
                            result[r] = UpdateOptions(True,n_cond,result[r])
                        this_layer.append(result[r])
                    # then add it all to this_layer

            # anything after this test in the workflow needs this negative mod
            print(wf,"Adding",condition,"to negatives")
            negative_mods.append(condition)

        else:
            # just a dest or R or A
            if(test == 'R'):
                continue  # ugh, can't return cause we have other potential tests?
                            # but we can stop processing tests and return the rest of this_layer?

            elif(test == 'A'):
                blaa = Option()
                for n_cond in negative_mods:
                    blaa = UpdateOptions(True,n_cond,blaa)
                this_layer.append(blaa)  # Add a blank option set at this layer


            else: 
                result = DoMath(workflows,test)
                if(len(result) > 0):
                    for r in range(len(result)):
                        print("mod options for",result[r])
                        for n_cond in negative_mods:
                            result[r] = UpdateOptions(True,n_cond,result[r])
                        this_layer.append(result[r])
                print("Plus negative mods 2?")
                # append this 'test' to all results?
                # appending is just modificaiton of options and there's nothing to modify from
                # just a destination change
#                this_layer.extend(result)
    for l in this_layer:
        print(wf,"done",l.xmin,l.xmax,l.mmin,l.mmax,l.amin,l.amax,l.smin,l.smax)
                        
    return this_layer

def Calculate(results):
    for l in result:
        print(l.xmin,l.xmax,l.mmin,l.mmax,l.amin,l.amax,l.smin,l.smax)
    # unique them, not sure why we need to
    skip = list()
    for r in range(len(results)):
        if(r != len(results)-1):
            for i in range(r+1,len(results)):
                match = True
                if(results[r].smin != results[i].smin):
                    match = False
                if(results[r].smax != results[i].smax):
                    match = False                
                if(results[r].xmin != results[i].xmin):
                    match = False
                if(results[r].xmax != results[i].xmax):
                    match = False        
                if(results[r].amin != results[i].amin):
                    match = False
                if(results[r].amax != results[i].amax):
                    match = False                
                if(results[r].mmin != results[i].mmin):
                    match = False
                if(results[r].mmax != results[i].mmax):
                    match = False 
                if(match == True):
                    print("skip")
                    skip.append(i)
    print(skip)

    # How to handle overlap?
    # is that an issue if we have the right results?

    total = 0
    for i in range(len(results)):
        if(i not in skip):
            total += ((results[i].xmax - results[i].xmin + 1) *
                     (results[i].mmax - results[i].mmin + 1) *
                     (results[i].amax - results[i].amin + 1) *
                     (results[i].smax - results[i].smin + 1))
    return total


if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    (workflows,parts) = ParseLines(lines)

#    combos = dict()
#    GetCombos(combos,workflows,'in')

#    for c in combos:
#        print("c",c)
#        for d in combos[c]:
#            print("d",d)
#    exit()
    result = DoMath(workflows,"in")

    print(len(result))

    print("why do we have some duplicates?")
    print("we're also missing m > 1548")  # that could be because the next step is just accepted.

    print("Part 2:",Calculate(result))
    print("oh goddammit, they could have overlap")

#    total = 0
#    for part in parts:
#        accepted = ProcessPart(part,workflows,'in')
#        if(accepted):
#            total += part.x + part.m + part.a + part.s
#    print("Part 1:",total)

    # Part 2 is just about the workflows.
    # Still start a 'in'
# 143228698000000
# 167409079868000


