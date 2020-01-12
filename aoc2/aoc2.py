import IntComputer as IC

# Lecture fichier d'entrée
donnees = open("aoc2.txt",'r')
intlist = list(map(int,donnees.read().split(",")))
donnees.close()

# Part 1
intlist[1:3] = 12,2
part1 = IC.IntComputer(intlist,0)
print(part1.operate())

# Part 2
stop = False
for noun in range(len(intlist)):
    if not stop:
        for verb in range(len(intlist)):
            intlist[1:3] = noun,verb
            part2 = IC.IntComputer(intlist,0)
            try:
                if part2.operate() == 19690720:
                    print(100*noun+verb)
                    stop = True
            except:
                pass