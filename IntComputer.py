from collections import deque

class IntComputer:
    """ Classe IntComputer.

            __init__(intlist, inputValue = 0)

            addInput(inputValue)

            operate()

            trace()

            isOver()
    """

    def __init__(self, intlist, *inputValues):

        self.currentInput = deque([])
        for inputValue in inputValues:
            self.currentInput.append(inputValue)
        self.instructionSet = intlist[:]
        self.currentInstruction = 0
        self.lastOutput = None
        self.outputs = deque()
        self.relativeBase = 0

    def __getitem__(self,pos):
        return self.instructionSet[pos] if pos < len(self.instructionSet) else 0

    def __setitem__(self,pos,item):
        if pos >= len(self.instructionSet):
            self.instructionSet.extend([0] * (pos - len(self.instructionSet) + 1))
        self.instructionSet[pos] = item

    def getCurrentInt(self,offset = 0):
        return self[self.currentInstruction + offset]

    def getRelativeInt(self,offset = 0):
        return self[self.getCurrentInt(offset) + self.relativeBase]

    def getOutput(self):
        try:
            return self.outputs.popleft()
        except:
            return -1

    def add(self,arg1,arg2,arg3): # opcode 1
        self[arg3] = arg1 + arg2
        self.currentInstruction += 4
        return False

    def mult(self,arg1,arg2,arg3): # opcode 2
        self[arg3] = arg1 * arg2
        self.currentInstruction += 4
        return False

    def save(self,arg1): # opcode 3
        if len(self.currentInput) > 0:
            self[arg1] = self.currentInput.popleft()
            self.currentInstruction += 2
            return False
        else:
            return True

    def out(self,arg1): # opcode 4
        self.lastOutput = arg1
        self.outputs.append(self.lastOutput)
        self.currentInstruction += 2
        return False

    def jumpIfTrue(self,arg1,arg2): # opcode 5
        if arg1 !=0:
            self.currentInstruction = arg2
        else:
            self.currentInstruction += 3
        return False

    def jumpIfFalse(self,arg1,arg2): # opcode 6
        if arg1 ==0:
            self.currentInstruction = arg2
        else:
            self.currentInstruction += 3
        return False

    def isLessThan(self,arg1,arg2,arg3): # opcode 7
        self[arg3] = 1 if arg1 < arg2 else 0
        self.currentInstruction += 4
        return False

    def isEqual(self,arg1,arg2,arg3): # opcode 8
        self[arg3] = 1 if arg1 == arg2 else 0
        self.currentInstruction += 4
        return False

    def setRelativeBase(self,arg1): # opcode 9
        self.relativeBase += arg1
        self.currentInstruction += 2
        return False

    operations = { 1 : add,
                   2 : mult,
                   3 : save,
                   4 : out,
                   5 : jumpIfTrue,
                   6 : jumpIfFalse,
                   7 : isLessThan,
                   8 : isEqual,
                   9 : setRelativeBase}

    args = { 1 : 3,
             2 : 3,
             3 : 1,
             4 : 1,
             5 : 2,
             6 : 2,
             7 : 3,
             8 : 3,
             9 : 1}

    def addInput(self,inputValue):
        self.currentInput.append(inputValue)

    def isOver(self):
        return True if self.getCurrentInt() == 99 else False

    def _argGenerator(self,opcode,pos):
        """ Utilisé pour déterminer les arguments de l'instruction en cours"""
        pmode = (self.getCurrentInt()%10**(pos+2)) // 10**(pos+1)
        if (opcode == 3 or pos == 3) and pmode == 2:
            return self.getCurrentInt(pos) + self.relativeBase
        elif pmode == 2 and pos < 3:
            return self.getRelativeInt(pos)
        elif pmode == 0 and opcode !=3 and pos < 3:
            return self[self.getCurrentInt(pos)]
        elif pos == 3 and pmode == 1:
            return self.currentInstruction + pos
        else:
            return self.getCurrentInt(pos)

    def operate(self):
        """
        Lance le fonctionnement de l'ordinateur jusqu'à sa fin (opcode 99) ou jusqu'à \
            nécessiter une nouvelle entrée. Renvoie la dernière sortie obtenue.

        Returns
        -------
        entier
            Dernière sortie du programme.

        """
        while not self.isOver():
            opcode = self.getCurrentInt()%100
            if opcode in self.operations:
                if self.operations[opcode](self,*[self._argGenerator(opcode,i) for i in range(1,self.args[opcode]+1)]):
                    return self.lastOutput
            else:
                print("Erreur : ",self.getCurrentInt())
                return None
        return self[0] if self.lastOutput is None else self.lastOutput

    def trace(self):
        """
        Lance l'odinateur puis affiche toutes les sorties

        """
        self.operate()
        print(self.outputs)

class ASCIIComputer(IntComputer):
    def addInput(self,inputValue):
        for c in inputValue:
            self.currentInput.append(ord(c))

    def getOutput(self):
        try:
            val = self.outputs.popleft()
            return chr(val) if val < 128 else val
        except IndexError:
            return -1

    def operate(self):
        val = IntComputer.operate(self)
        if val >= 128:
            print("Résultat obtenu :\t",val)
        else:
            feed = "".join(map(chr,list(self.outputs)))
            print(feed)

