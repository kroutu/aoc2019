import os
os.chdir("C:/Users/alexa/Desktop/Python/aoc2019/aoc1")

# Lecture fichier d'entrée
donnees = open("aoc1.txt",'r')
masses = map(int,donnees.read().split("\n"))
donnees.close()

TOT = 0
for masse in masses:
    fuel = masse//3 - 2
    total = fuel
    while fuel//3 - 2 >0:
        fuel = fuel//3-2
        total+=fuel
    TOT += total

print(TOT)