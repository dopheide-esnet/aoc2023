#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def GetRaces(lines):    
    (trash,times) = lines[0].split(":")
    times = times.split(" ")
    times = [int(i) for i in times if i]
    (trash,distances) = lines[1].split(":")
    distances = distances.split(" ")
    distances = [int(i) for i in distances if i]
    print(times)
    print(distances)
    return(times,distances)

def GetWays(t,d):
    print(t,d)

    ways = 0
    for hold in range(1,t):
        distance = hold * (t-hold)
#        print(hold, distance)
        if(distance > d):
            ways += 1

    return ways

if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    (times, distances) = GetRaces(lines)

#    total = 1
#    for race in range(len(times)):
#        ways = GetWays(times[race],distances[race])
#        print(ways)
#        total *= ways
#    print(total)

    one_time = ""
    one_distance = ""
    for i in range(len(times)):
        one_time += str(times[i])
        one_distance += str(distances[i])

    one_time = int(one_time)
    one_distance = int(one_distance)

    ways = GetWays(one_time,one_distance)
    print(ways)


