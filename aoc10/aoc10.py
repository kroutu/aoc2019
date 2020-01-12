import cmath
from math import pi

# Lecture fichier d'entrée
donnees = open("aoc10.txt",'r')
champ = donnees.read().splitlines()
donnees.close()

def phase(z):
    phi = cmath.phase(z)
    return phi if phi <= pi/2 else phi - 2 * pi

def trouverAngles(x,y):
    angles = set(cmath.phase(complex(x-xd,yd-y)) for xd in range(len(champ)) \
                                                 for yd in range(len(champ[0])) \
                                                 if champ[yd][xd] == "#")
    return len(angles)

en_vue = [(trouverAngles(x,y),x,y) for x in range(len(champ)) \
                                   for y in range(len(champ[0])) \
                                   if champ[y][x] == "#"]
part1,xc,yc = max(en_vue)

angles = [(phase(complex(x-xc,yc-y)),x,y) for x in range(len(champ)) \
                                          for y in range(len(champ[0])) \
                                          if champ[y][x] == "#"]
angles.sort(reverse = True)
distinct_angles = list(set(item[0] for item in angles))
distinct_angles.sort(reverse = True)

candidates = [(asteroid[1],asteroid[2]) for asteroid in angles if asteroid[0]==distinct_angles[199]]