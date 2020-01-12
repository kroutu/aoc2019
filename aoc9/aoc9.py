import IntComputer as IC

# Lecture fichier d'entrée
donnees = open("aoc9.txt",'r')
intlist = list(map(int,donnees.read().split(",")))
donnees.close()

part1 = IC.IntComputer(intlist,1)
print(part1.operate())

part2 = IC.IntComputer(intlist,2)
print(part2.operate())