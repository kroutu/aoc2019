from itertools import combinations
from math import gcd

class Moon:
    def __init__(self,x,y,z):
        self.coordinates = [x,y,z]
        self.velocity = [0]*3

    def updateSpeed(self,other,i):
        if other.coordinates[i] < self.coordinates[i]:
            return self.velocity[i] - 1
        elif other.coordinates[i] > self.coordinates[i]:
            return self.velocity[i] + 1
        else:
            return self.velocity[i]

    def gravity(self,other):
        self.velocity = [self.updateSpeed(other,i) for i in range(3)]

    def move(self):
        self.coordinates = [self.coordinates[i] + self.velocity[i] for i in range(3)]

    def moveAxis(self,index):
        self.coordinates[index] += self.velocity[index]

    def calcEnergy(self):
        pot = 0
        for c in self.coordinates:
            pot += abs(c)
        kin = 0
        for v in self.velocity:
            kin += abs(v)
        return pot * kin

test1 = [-1,0,2,2,-10,-7,4,-8,8,3,5,-1]
test2 = [-8,-10,0,5,5,10,2,-7,3,9,-8,-3]
aoc = [-14,-4,-11,-9,6,-7,4,1,4,2,-14,-9 ]

moons = [Moon(*aoc[i:i+3]) for i in range(0,10,3)]
Io, Europa, Ganymede, Callisto = moons

def longueurCycle(axis):
    moons = [Moon(*aoc[i:i+3]) for i in range(0,10,3)]
    Io, Europa, Ganymede, Callisto = moons
    step = 0
    boucle = False
    while not boucle:
        for moon1, moon2 in combinations(moons,2):
            moon1.velocity[axis] = moon1.updateSpeed(moon2,axis)
            moon2.velocity[axis] = moon2.updateSpeed(moon1,axis)
        for moon in moons:
            moon.moveAxis(axis)
        step += 1
        if step > 1:
            for i,moon in enumerate(moons):
                boucle = moon.velocity[axis] == 0 and moon.coordinates[axis] == aoc[3*i+axis]
                if not boucle:
                    break
    return step

def ppcm(a,b):
    a //= gcd(a,b)
    return a*b

step = 0
while step < 1000:
    for moon1, moon2 in combinations(moons,2):
        moon1.gravity(moon2)
        moon2.gravity(moon1)
    for moon in moons:
        moon.move()
    step += 1
part1 = 0
for moon in moons:
    part1 += moon.calcEnergy()
print(part1)

cycles = [longueurCycle(i) for i in range(3)]
étape = ppcm(cycles[0],cycles[1])
print(ppcm(cycles[2],étape))


