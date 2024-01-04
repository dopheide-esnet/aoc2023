#!/usr/bin/env python3

testcase = True
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True


if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    print(lines)


