import time

def simpl():
    # Extraction
    commandes = []
    valeurs = []
    for ligne in todo:
        *u, cmd, n = ligne.split()
        try:
            n = int(n)
        except:
            cmd = n
            n = 0
        commandes.append(cmd)
        valeurs.append(n)
    # Simplification stack / cut
    offset = 0
    stack = commandes.index("stack")
    while stack != -1:
        if stack + 2 < len(commandes) and commandes[stack+1] == "cut" and commandes[stack+2]=="stack":
            valeurs[stack+1] *= -1
            commandes.pop(stack+2)
            valeurs.pop(stack+2)
            commandes.pop(stack)
            valeurs.pop(stack)
        else:
            offset = stack + 1
        try:
            stack = commandes.index("stack",offset)
        except:
            stack = -1
    # Simplification cut
    offset = 0
    stack = commandes.index("cut")
    while stack != -1:
        if stack + 1 < len(commandes) and commandes[stack+1] == "cut":
            valeurs[stack] += valeurs[stack+1]
            commandes.pop(stack+1)
            valeurs.pop(stack+1)
        else:
            offset = stack + 1
        try:
            stack = commandes.index("cut",offset)
        except:
            stack = -1
    return commandes, valeurs

def part1():
    def reverse(deck, n):
        return list(reversed(deck))

    def increment(deck, n):
        end = [-1]*len(deck)
        for ideck,iend in enumerate(range(0,n*len(deck),n)):
            end[iend%len(deck)] = deck[ideck]
        return end

    def cut(deck,n):
        if n > 0:
            deck.extend(deck[:n])
            del deck[:n]
        else:
            deck[0:0] = deck[len(deck)+n:]
            del deck[len(deck)+n:]
        return deck

    techs = {"stack"        : reverse,
             "increment"    : increment,
             "cut"          : cut}

    deck = list(range(10007))
    pos = [2019]
    for cmd,n in zip(commandes, valeurs):
        deck = techs[cmd](deck,n)
        pos.append(deck.index(2019))
    print("Partie 1 :\t\t", deck.index(2019))
    return pos

def part2(vrai, pos):
    def rev_rev(ind, n):
        return taille - ind - 1

    def rev_inc(ind, n):
        for iend in range(ind,n*taille,taille):
            if iend%n == 0:
                return iend // n

    def rev_cut(ind,n):
        if (n > 0 and ind < taille - n) or -ind <= n < 0:
            return ind + n
        if n > 0:
            return ind - taille + n
        if n < 0:
            return ind + taille + n

    techs = {"stack"        : rev_rev,
             "increment"    : rev_inc,
             "cut"          : rev_cut}

    ind = 2020 if vrai else 6638
    taille = 119315717514047 if vrai else 10007
    pos.reverse()
    for _ in range(101741582076661):
        for i,ligne in enumerate(reversed(todo)):
            *u, cmd, n = ligne.split()
            try:
                n = int(n)
            except:
                cmd = n
            ind = techs[cmd](ind,n)
        if not vrai:
            break
    print(ind)


T0 = time.perf_counter()

donnees = open("aoc22.txt",'r')
todo = donnees.read().splitlines()
donnees.close()
commandes, valeurs = simpl()
pos = part1()
T1 = time.perf_counter()
print("Temps partie 1 :\t", T1-T0)

part2(False,pos)
T2 = time.perf_counter()
print("Temps partie 2 :\t", T2-T1)