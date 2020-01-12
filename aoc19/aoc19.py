import IntComputer as IC
import time
from itertools import product, count

def afficher():
    for ligne in plan:
        print("".join(list(ligne)))

def getCase(x,y):
    rajout = False
    try:
        etat = plan[y][x]
        if etat not in ".#":
            rajout = True
        else:
            etat = 0 if etat =='.' else 1
    except:
        rajout = True
    if rajout:
        if y == len(plan):
            plan.append(list(" "*len(plan[y-1])))
        if x == len(plan[y]):
            plan[y].append(" ")
        drone = IC.IntComputer(intlist, x, y)
        etat = drone.operate()
        plan[y][x] = "#" if etat == 1 else "."
    return etat

def squareSearch(xmin,ymin):
    xmax = xmin + 100
    ymax = ymin + 100
    for i in range(xmin, xmax):
        for j in range(ymin,ymax):
            if getCase(i,j) == 0:
                return False
    return True

T0 = time.perf_counter()

# Lecture fichier d'entrée
donnees = open("aoc19.txt",'r')
intlist = list(map(int,donnees.read().split(",")))
donnees.close()

total = 0
plan = [['']*50 for _ in range(50)]
for x,y in product(range(50), repeat = 2):
    drone = IC.IntComputer(intlist, x, y)
    etat = drone.operate()
    total += etat
    plan[y][x] = '#' if etat == 1 else '.'

afficher()
print("Partie 1 :\t\t",total)
T1 = time.perf_counter()
print("Temps partie 1 :\t",T1-T0)
stop = False
next_start = 30
for y in count(50):
    if stop:
        break
    debut_rayon = False
    for x in count(next_start):
        etat = getCase(x,y)
        if etat == 1:
            if not debut_rayon:
                debut_rayon = True
                next_start = x
            stop = squareSearch(x,y)
            if stop:
                print("Partie 2 :\t", 10000*x+y)
                stop = True
                break
        elif debut_rayon:
            break

T2 = time.perf_counter()
print("Temps partie 2 :\t",T2-T1)