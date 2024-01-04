#!/usr/bin/env python3
import re

testcase = False
if testcase:
    file = "test3.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def NumberizeMin(line):
    numbers = {'one': '1','two': '2','three': '3','four': '4','five': '5',
               'six': '6','seven': '7','eight':'8','nine':'9'}
    min = -1
    val = ''
    for num in numbers:
        loc = line.find(num)
        if(loc >= 0):
            if(min < 0) or (loc < min):
                min = loc
                val = num

    if(min >= 0):
        line = line.replace(val,numbers[val],1)
    return line

def NumberizeMax(line):
    numbers = {'one': '1','two': '2','three': '3','four': '4','five': '5',
               'six': '6','seven': '7','eight':'8','nine':'9'}
    max = -1
    val = ''
    for num in numbers:
        loc = line.rfind(num)
        if(loc >= 0):
            if(max < 0) or (loc > max):
                max = loc
                val = num

    if(max >= 0):
        line = numbers[val].join(line.rsplit(val, 1))
#        line.replace(val,numbers[val],1)
    return line


if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()

    re_num1 = re.compile(r'^[a-z]*(\d)')
    re_num2 = re.compile(r'(\d)[a-z]*$')
    total = 0
    total2 = 0
    for line in lines:
        print(line)

        line2 = NumberizeMin(line)
        line3 = NumberizeMax(line)

        # Part 1
        m = re_num1.search(line)
        if(m):
            num1 = m.group(1)
            m = re_num2.search(line)
            if(m):
                num2 = m.group(1)
                num = str(num1) + str(num2)
                val = int(num)
                total += val

        # Part 2
        m = re_num1.search(line2)
        if(m):
            num1 = m.group(1)
            m = re_num2.search(line3)
            if(m):
                num2 = m.group(1)
                num = str(num1) + str(num2)
                val = int(num)
                print(val)
                total2 += val

    print("Part 1:",total)
    print("Part 2:",total2)



