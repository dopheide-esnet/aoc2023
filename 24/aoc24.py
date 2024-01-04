#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def TestWorks():
    return True

def InputEq(lines):
    # 19, 13, 30 @ -2,  1, -2
    eq = list()
    for line in lines:
        m = re.search(r'(\d+), (\d+), (\d+) \@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)', line)
        if(m):
            x = int(m.group(1))
            y = int(m.group(2))
            z = int(m.group(3))
            vx = int(m.group(4))
            vy = int(m.group(5))
            vz = int(m.group(6))
            eq.append((x,y,z,vx,vy,vz))
        else:
            print("what?")
            exit()
    return eq

def Solve(e1,e2):
#    print(e1,e2)

    (x,y,z,vx,vy,vz) = e1
    (x2,y2,z2,vx2,vy2,vz2) = e2

    m1 = vy / vx
    m2 = vy2 / vx2

    if(m1 == m2):
        print("parallel")
        return (False,(0,0))
    
    c1 = y-(m1*x)
    c2 = y2-(m2*x2)
    sx = (c1-c2)/(m2-m1)
    sy = m1*sx+c1

    if(sx >= 200000000000000 and sx <= 400000000000000 and sy >= 200000000000000 and sy <= 400000000000000):

#        print("Intesect in range")
#        print("Future or past?")
        # what if it's a vertical or horizontal line?
        if(vx == 0 or vy == 0):
            print("ugh")
            exit()
        if((sx <= x and vx < 0) or (sx >= x and vx > 0)): # vx headed towards intersection in future
            if((sx <= x2 and vx2 < 0) or (sx >= x2 and vx2 > 0)):
                return (True,(sx,sy))
    
    return (False,(0,0))

if(__name__ == '__main__'):

    try:
        stuff = open(file,"r")
    except FileNotFoundError:
        print("Gonna need an input file there, Bud.")
        exit(0)
    else:
        with stuff:
            lines = stuff.read().splitlines()
    

    equations = InputEq(lines)

    total = 0
    for i in range(len(equations)-1):  # right?
        for j in range(i+1,len(equations)):
            (result,(x,y)) = Solve(equations[i],equations[j])
            if(result):
                total += 1

    print("Part1",total)

    exit()
    (x,y) = (19,13)
    (vx,vy) = (-2,1)
    (vx2,vy2) = (-1,-1)
    (x2,y2) = (18,19)


    (x,y) = (20,25)
    (vx,vy) = (-2,-2)

    (vx2,vy2) = (-1,-1)
    (x2,y2) = (18,19)

    m1 = vy / vx
    m2 = vy2 / vx2

    # If m1 == m2, never itersect
    
    c1 = y-(m1*x)
    c2 = y2-(m2*x2)

    print("m1,m2,c1,c2",m1,m2,c1,c2)

    sx = (c1-c2)/(m2-m1)
    sy = m1*sx+c1
    print("sx sy",sx,sy)



#    L1 = (1, 2, -25)
#    L2 = (1,1,1)

#    a1, b1, c1 = L1
#    a2, b2, c2 = L2

#    A = np.array([[-a1, -b1], [-a2, -b2]])
#    B = np.array([c1, c2])
#    X = np.linalg.solve(A, B)

#    print('The intersection point is at', X)

    # Part 1




