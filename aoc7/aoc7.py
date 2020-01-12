import IntComputer as IC
import itertools

def tryPhaseSeq1(phaseSeq):
    value = 0
    for i in range(5):
        amp = IC.IntComputer(intlist,phaseSeq[i])
        amp.addInput(value)
        value = amp.operate()
    return value

def tryPhaseSeq2(phaseSeq):
    amps = [IC.IntComputer(intlist,phase) for phase in phaseSeq]
    value = 0
    for i in itertools.cycle(range(5)):
        amps[i].addInput(value)
        value = amps[i].operate()
        if amps[4].isOver():
            return value

# Lecture fichier d'entrée
donnees = open("aoc7.txt",'r')
intlist = list(map(int,donnees.read().split(",")))
donnees.close()

# Part 1
outputs = [tryPhaseSeq1(phaseSeq) for phaseSeq in itertools.permutations(range(5))]
print(max(outputs))

# Part 2
outputs = [tryPhaseSeq2(phaseSeq) for phaseSeq in itertools.permutations(range(5,10))]
print(max(outputs))