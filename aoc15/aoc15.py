import time
import IntComputer as IC

def getMove(pos,trajet):
    x,y = pos
    adj = [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]
    for p in adj:
        if p not in trajet and coord.setdefault(p,-1) < 0:
            return p, adj.index(p)+1
    return trajet[-2], adj.index(trajet[-2])+1

def afficher(plan,position,status):
    print("Robot en case",position,"après statut",status)
    for ligne in plan:
        print("".join(ligne))
    print()

def findOxygen(max_length, explo):
    repair_robot = IC.IntComputer(intlist)
    status = 0
    position = (21,21)
    plan[21][21] = "R"
    trajet = [(21,21)]
    while status != 2 or explo:
        try:
            next_position, dep = getMove(position,trajet)
        except:
            break
        repair_robot.addInput(dep)
        status = repair_robot.operate()
        coord[next_position] = status
        if status > 0:
            if plan[position[1]][position[0]] != "O":
                plan[position[1]][position[0]] = "."
            position = next_position
            if len(trajet)>1 and position == trajet[-2]:
                del trajet[-1]
            else:
                trajet.append(position)
            plan[position[1]][position[0]] = "R" if status == 1 else "O"
            plan[21][21] = "S"
        else:
            plan[next_position[1]][next_position[0]] = "#"
        if explo and status == 2:
            safe.append(position)
            print("Partie 1 :\t",len(trajet)-1)
        #afficher(plan,position,status)

def getVides(pos,depth):
    x,y = pos
    adj = [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]
    for p in adj:
        if coord[p] == 1:
            yield p
        elif coord[p] == 2:
            if p not in temps.keys() or temps[p] > depth+1:
                yield p

def remplissage(pos, depth = 0):
    if pos not in temps.keys() or temps[pos] > depth:
        temps[pos] = depth
    vides_adj = [case for case in getVides(pos,depth)]
    if len(vides_adj) == 0:
        temps[pos] = depth
        return
    for case in vides_adj:
        coord[case] = 2
        remplissage(case, depth+1)


t0 = time.perf_counter()
# Lecture fichier d'entrée
donnees = open("aoc15.txt",'r')
intlist = list(map(int,donnees.read().split(",")))
donnees.close()

coord = {(21,21) : 1}
plan = [[" "]*45 for _ in range(41)]
plan[21][21] = "R"
meilleur_chemin = 999
safe = []
findOxygen(meilleur_chemin,True)
temps = {}

t1 = time.perf_counter()
print("Temps exploration :\t", t1-t0)

taille_oxygene = list(coord.values()).count(1)+1
remplissage(safe[0])
print("Partie 2 :\t",max(list(temps.values())))

t2 = time.perf_counter()
print("Temps récursion :\t", t2-t1)



