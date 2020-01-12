import IntComputer as IC

# Lecture fichier d'entrée
donnees = open("aoc5.txt",'r')
intlist = list(map(int,donnees.read().split(",")))
donnees.close()

part1 = IC.IntComputer(intlist,1)
part2 = IC.IntComputer(intlist,5)

print(part1.operate())
print(part2.operate())