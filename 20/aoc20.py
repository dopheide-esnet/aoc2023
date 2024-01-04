#!/usr/bin/env python3

import math

testcase = False
if testcase:
    file = "test2.txt"
else:
    file = "input.txt"

queue = list()
low_pulse = 0
high_pulse = 0
part2 = {'ct': list(),'kp': list(),'ks': list(),'xc': list()}

def TestWorks():
    return True

class FlipFlop():
    def __init__(self,name,dest):
        self.name = name
        self.type = "%"
        self.state = 0
        self.dest = dest  # pulse destinations

class Conjunction():
    def __init__(self,name,dest):
        self.name = name
        self.type = "&"
        self.dest = dest
        self.inputs = dict()  # dict of input modules and their states, starting at low
    
class Broadcaster():
    def __init__(self,name,dest):
        self.name = name
        self.type = "B"
        self.dest = dest

def BuildMachines(lines):
    machines = dict()

    for line in lines:
        line = line.replace(" ", "")
        (blaa,dest) = line.split("->")
        dests = dest.split(',')
        name = blaa[1:]
        if(blaa[0] == "%"):
            machines[name] = FlipFlop(name,dests)
        elif(blaa[0] == "&"):
            machines[name] = Conjunction(name,dests)
        else:
            machines['broadcaster'] = Broadcaster(name,dests)

    # run back through and check flipflop dest's for conjunctions and populate their memory tables.
    for m in machines:
        if(machines[m].type == '%' or machines[m].type == '&'):
            for d in machines[m].dest:
                if d in machines:
                    if(machines[d].type == '&'):
                        machines[d].inputs[m] = 0  # set initial input low
    return machines

def DoPulse(machines,button_num):
    '''
    For part 2 we try to track the outputs of the four conjunctions ahead of rx
    &ct -> bb
    &kp -> bb
    &ks -> bb
    &bb -> rx
    &xc -> bb
    '''

    global queue
    global low_pulse
    global high_pulse
    global part2

#    print("Q:",queue)
    (source,target,signal) = queue.pop(0)

    if(signal == 0):
        low_pulse += 1
    else:
        high_pulse += 1

#    print(source,signal,"->",target)

    if(target == "output"):
#        print("test case target, do nothing")
        return False
    
    if(target == "rx"):
        if(signal == 0):
            return True
        else:
            return False

    if(machines[target].type == '%'):
        if(signal == 1):
            return False # do nothing with a high signal
        else:
            if(machines[target].state == 0):
                # send high pulse to dests
                pulse = 1
                machines[target].state = 1
            else:
                # send low pulse to dests
                pulse = 0
                machines[target].state = 0
            for d in machines[target].dest:
                queue.append((target,d,pulse))
    elif(machines[target].type == '&'):
        if(source not in machines[target].inputs):
            print("Shouldn't get here",source,target)
            exit()
        machines[target].inputs[source] = signal  # set memory to new signal
        pulse = 0
        for i in machines[target].inputs:
            if(machines[target].inputs[i] == 0): # if any of the inputs are low, we send high
                pulse = 1
                if(target in part2):
                    part2[target].append(button_num)
                break
        for d in machines[target].dest:
            queue.append((target,d,pulse))
    else:  # must be the broadcast
        if(machines[target].type != 'B'):
            print("Whut?")
            exit()
        for d in machines[target].dest:
            queue.append((target,d,signal))  # repeat same signal

    return False

if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    machines = BuildMachines(lines)

#    for m in machines:
#        if(machines[m].type == '%'):
#            print("Flipflop",m,machines[m].state,machines[m].dest)
#        elif(machines[m].type == '&'):
#            print("Conjunction",m,machines[m].inputs,machines[m].dest)
#        else:
#            print("Broadcast",0,machines[m].dest)

    # TODO might have to save when the same/(possibly) starting state is reached again
    #  

#    button = 1000

#    for b in range(button):
        # PressButton
    b = 1
    while(b < 5000):
        print("Button Press",b)
        queue.append(("dop","broadcaster",0)) # set broadcast a low pulse in the queue 

        while(len(queue)> 0):
        # WHILE len(queue) > LOOP
            DoPulse(machines,b)
        b += 1

    print("Part1",high_pulse * low_pulse)
    print("Part2",part2)
    mult = list()
    for p in part2:
        mult.append(part2[p][0])


    print(math.lcm(*mult))

