import IntComputer as IC
import time

T0 = time.perf_counter()

# Lecture fichier d'entrée
donnees = open("aoc21.txt",'r')
Intlist = list(map(int,donnees.read().split(",")))
donnees.close()
del donnees

Robot = IC.ASCIIComputer(Intlist)
Robot.addInput("NOT A J"+"\n"+\
               "NOT B T"+"\n"+\
               "OR T J" +"\n"+\
               "NOT C T"+"\n"+\
               "OR T J" +"\n"+\
               "AND D J"+"\n"+\
               "WALK"   +"\n")
Robot.operate()

T1 = time.perf_counter()
print("Temps partie 1 :\t", T1-T0)

Robot = IC.ASCIIComputer(Intlist)
Robot.addInput("NOT A J"+"\n"+\
               "NOT B T"+"\n"+\
               "OR T J" +"\n"+\
               "NOT C T"+"\n"+\
               "OR T J" +"\n"+\
               "AND D J"+"\n"+\
               "OR I T" +"\n"+\
               "AND E T"+"\n"+\
               "OR H T" +"\n"+\
               "AND T J"+"\n"+\
               "RUN"    +"\n")
Robot.operate()

T2 = time.perf_counter()
print("Temps partie 2 :\t", T2-T1)