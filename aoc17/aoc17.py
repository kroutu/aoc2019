import IntComputer as IC
import time
from itertools import product

T0 = time.perf_counter()

def adj(x,y):
    liste = []
    if y != 0:
        liste.append(plan[y-1][x])
    if y != len(plan) - 1:
        liste.append(plan[y+1][x])
    if x != 0:
        liste.append(plan[y][x-1])
    if x != len(plan[0]) - 1:
        liste.append(plan[y][x+1])
    return liste

def lireTerrain():
    c = Robot.getOutput()
    while c!= -1:
        yield c
        c = Robot.getOutput()

def getIntersections():
    for y, ligne in enumerate(plan):
        for x, c in enumerate(ligne):
            if c == '#' and all(v == '#' for v in adj(x,y)):
                yield x, y

def intersect(d,x,y):
    for direction in FACING:
        if direction != d and direction != FACING[FACING.index(d)-2]:
            if y+COORD[direction][1] >= 0 and x+COORD[direction][0] >= 0:
                try:
                    if plan[y+COORD[direction][1]][x+COORD[direction][0]] == '#':
                        return COORD[direction], "R" if (FACING.index(direction)-FACING.index(d))%4 == 1 \
                            else "L"
                except:
                    continue
    return None, None

def getTrajet():
    chemin = ""
    for x,y in product(range(len(plan[0])),range(len(plan))):
        if plan[y][x] != '#' and plan[y][x] != '.':
            xs,ys = x,y
            del x,y
            break
    dc, turn = intersect("U",xs,ys)
    while turn != None:
        distance = 0
        chemin += turn + ","
        try:
            while plan[ys+dc[1]][xs+dc[0]] == '#':
                xs,ys = xs+dc[0],ys+dc[1]
                distance+=1
        except:
            pass
        chemin += str(distance)+","
        dc, turn = intersect(RCOORD[dc],xs,ys)
    return chemin[:len(chemin)-1]

def ind(s):
    indf = 20
    if "A" in s:
        indf = min(s.index('A'),indf)
    if "B" in s:
        indf = min(s.index('B'),indf)
    if "C" in s:
        indf = min(s.index('C'),indf)
    return indf

def deeper(s, level):
    ifin = ind(s)
    for i, c in enumerate(reversed(s[:ifin])):
        if c in ",LR" or s[ifin-i]!=",":
            continue
        test = s[:ifin-i]
        snext = s.replace(test,level).lstrip("ABC,")
        yield test, snext

def findExpr(s):
    iA = deeper(s,"A")
    for testA, sbis in iA:
        iB = deeper(sbis,"B")
        for testB, ster in iB:
            iC = deeper(ster,"C")
            for testC, sfinal in iC:
                if len(sfinal) == 0:
                    return testA+"\n", testB+"\n", testC+"\n", s.replace(testA,"A").replace(testB,"B").replace(testC,"C")+"\n"

# Lecture fichier d'entrée
donnees = open("aoc17.txt",'r')
Intlist = list(map(int,donnees.read().split(",")))
donnees.close()
del donnees

Robot = IC.ASCIIComputer(Intlist)
Robot.operate()
Plan_str = "".join(c for c in lireTerrain())
plan = [ligne for ligne in Plan_str.split("\n") if len(ligne)>0]
Alignment = sum(x*y for x,y in getIntersections())

print("Partie 1 :\t\t",Alignment)
T1 = time.perf_counter()
print("Temps partie 1 :\t",T1-T0)

FACING = "URDL"
COORD = {'U' : (0,-1), 'R' : (1,0), 'D' : (0,1), 'L' : (-1,0)}
RCOORD = {COORD[key] : key for key in COORD.keys()}

Robot2 = IC.ASCIIComputer(Intlist)
Robot2[0] = 2
chemin = getTrajet()
rA, rB, rC, rG = findExpr(chemin)
Robot2.addInput(rG+rA+rB+rC+"n\n")

Robot2.operate()
T2 = time.perf_counter()
print("Temps partie 2 :\t",T2-T1)