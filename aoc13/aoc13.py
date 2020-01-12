import IntComputer as IC
import time

class Game(IC.IntComputer):
    tiles = {0 : " ",
             1 : "#",
             2 : "X",
             3 : "T",
             4 : "O"}
    def setMovable(self,x,t):
        if self.tiles[t]=="T":
            self.pad = x
        elif self.tiles[t]=="O":
            self.ball = x

    def setField(self):
        IC.IntComputer.operate(self)
        resultats = tuple((self.getOutput(),self.getOutput(),self.getOutput()) \
                  for _ in range(len(self.outputs)//3))
        x,y,tile = zip(*resultats)
        self.field = [[" "]*(max(x)+1) for _ in range(max(y)+1)]
        for xc,yc,tc in resultats:
            self.field[yc][xc] = self.tiles[tc]
            self.setMovable(xc,tc)
        self.nextMove = -1
        return self.field

    def timeStep(self):
        IC.IntComputer.addInput(self,self.nextMove)
        IC.IntComputer.operate(self)
        try:
            resultats = tuple((self.getOutput(),self.getOutput(),self.getOutput()) \
                  for _ in range(len(self.outputs)//3))
            x,y,tile = zip(*resultats)
        except:
            self.score = -1
            self.field.clear()
            return
        for xc,yc,tc in resultats:
            if xc == -1 and yc ==0:
                self.score = tc
            else:
                self.setMovable(xc,tc)
                self.field[yc][xc] = self.tiles[tc]
        if abs(self.pad - self.ball) < 1:
            self.nextMove = 0
        elif self.pad < self.ball:
            self.nextMove = 1
        else:
            self.nextMove = -1
        return self.field

    def playing(self):
        for ligne in self.field:
            for case in ligne:
                if case == "X":
                    return True
        return False

    def __repr__(self):
        string = ""
        for ligne in self.field:
            string += "".join(list(ligne)) + "\n"
        return string

t0 = time.perf_counter()
# Lecture fichier d'entrée
donnees = open("aoc13.txt",'r')
intlist = list(map(int,donnees.read().split(",")))
donnees.close()

# Part 1
BreakOut = Game(intlist)
terrain = BreakOut.setField()
part1 = 0
for ligne in terrain:
    part1 += ligne.count("X")
print(part1)

# Part 2
intlist[0] = 2
BreakOut = Game(intlist)
BreakOut.setField()
while BreakOut.playing():
    BreakOut.timeStep()

print(BreakOut.score)
print(time.perf_counter()-t0)