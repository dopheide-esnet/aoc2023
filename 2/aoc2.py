#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def PlayGame(line,mr,mg,mb):

    # parse input
    (g,i) = line.split(":")
    (g,id) = g.split(" ")
    id = int(id)
    hands = i.split(";")
    my_mr = 0
    my_mg = 0
    my_mb = 0
    for hand in hands:
        red = 0
        green = 0
        blue = 0
        m = re.search(r'(\d+) red',hand)
        if(m):
            red = int(m.group(1))
        m = re.search(r'(\d+) green',hand)
        if(m):
            green = int(m.group(1))
        m = re.search(r'(\d+) blue',hand)                    
        if(m):
            blue = int(m.group(1))

        if(red > my_mr):
            my_mr = red
        if(green > my_mg):
            my_mg = green
        if(blue > my_mb):
            my_mb = blue

    power = my_mr * my_mg * my_mb        

# For Part 1
#        if red > mr or green > mg or blue > mb:
#            return 0

    return power
#    return id

if(__name__ == '__main__'):
    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    possible = 0
    for line in lines:
        if(":" in line):
            id = PlayGame(line,12,13,14)
            possible += id
            print(id)

    print(possible)

