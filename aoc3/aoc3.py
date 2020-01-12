import os
os.chdir("C:/Users/alexa/Desktop/Python/aoc2019/aoc3")

# Renvoie : tailleH, tailleV, centreH, centreV
def tailleGrilleFil(fil):
    posH = [0]
    posV = [0]

    # Construction de la liste des positions successives par rapport au départ
    for section in fil:
        if section[0]=="U":
            posV.append(posV[len(posV)-1] - section[1])
        elif section[0]=="D":
            posV.append(posV[len(posV)-1] + section[1])
        elif section[0]=="L":
            posH.append(posH[len(posH)-1] - section[1])
        elif section[0]=="R":
            posH.append(posH[len(posH)-1] + section[1])

    return min(posH), max(posH), min(posV), max(posV)
    return minH + maxH +1, minV + maxV + 1, abs(minH), abs(minV)

def initGrilleFil(fil1,fil2):
    minH1,maxH1,minV1,maxV1 = tailleGrilleFil(fil1)
    minH2,maxH2,minV2,maxV2 = tailleGrilleFil(fil2)
    minH, minV = min(minH1,minH2), min(minV1,minV2)
    maxH, maxV = max(maxH1,maxH2), max(maxV1,maxV2)
    grille = [[0]*(abs(minH) + abs(maxH) + 1) for i in range(abs(minV) + abs(maxV) + 1)]
    centreH, centreV = abs(min(minH1,minH2)), abs(min(minV1,minV2))
    grille[centreV][centreH] = "?"
    return grille, centreH, centreV

def afficherGrille(grille):
            for i in range(len(grille)):
                for j in range(len(grille[0])):
                    print(grille[i][j],end="")
                print()
            print()

# Lecture fichier d'entrée
donnees = open("aoc3.txt",'r')
fil1Brut,fil2Brut = donnees.read().split("\n")
donnees.close()

fil1str = fil1Brut.split(",")
fil2str = fil2Brut.split(",")

# Données fil : tuple (direction, distance)
fil1 = [(section.rstrip("0123456789"),int(section.lstrip("ULRD"))) for section in fil1str]
fil2 = [(section.rstrip("0123456789"),int(section.lstrip("ULRD"))) for section in fil2str]

grille, X, Y = initGrilleFil(fil1,fil2)

currentPosX, currentPosY = X, Y
longueur = 0

for section in fil1:
    for i in range(section[1]):
        longueur += 1
        if section[0]=="U":
            currentPosY -= 1
        elif section[0]=="D":
            currentPosY += 1
        elif section[0]=="L":
            currentPosX -= 1
        elif section[0]=="R":
            currentPosX += 1
        if grille[currentPosY][currentPosX] == 0:
            grille[currentPosY][currentPosX] = longueur

currentPosX, currentPosY = X, Y
intersections = []
steps = []
longueur = 0

for section in fil2:
    for i in range(section[1]):
        longueur += 1
        if section[0]=="U":
            currentPosY -= 1
        elif section[0]=="D":
            currentPosY += 1
        elif section[0]=="L":
            currentPosX -= 1
        elif section[0]=="R":
            currentPosX += 1
        if grille[currentPosY][currentPosX] > 0:
            intersections.append((currentPosX, currentPosY))
            steps.append(longueur + grille[currentPosY][currentPosX])

print(min([abs(cross[0] - X) + abs(cross[1] - Y) for cross in intersections]))
print(min(steps))
