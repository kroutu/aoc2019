# Lecture fichier d'entrée
donnees = open("aoc6.txt",'r')
relations = donnees.read().splitlines()
duos = [paire.split(")") for paire in relations]
for paire in duos:
    paire.reverse()
relDict = dict(duos)
donnees.close()

def drawGalaxy():
    from PIL import Image,ImageDraw
    image = Image.new("P",(800,800),"black")
    draw = ImageDraw.Draw(image)
    draw.arc([20,20,320,320], 0, 360,"white", 2)
    image.show()
    

def getSize(duos):
    total = 0
    planetsToExplore = ["COM"]
    depth = 0

    while len(planetsToExplore) > 0:
        explored = []
        depth += 1
        for planet in planetsToExplore:
            explored += [rel[0] for rel in duos if planet == rel[1]]

        total += depth * len(explored)
        planetsToExplore = explored

    return total

def getPath(dic,target):
    path = [target]
    while path[len(path)-1] != "COM":
        path.append(dic[path[len(path)-1]])
    return set(path)

print(getSize(duos))

youPath = getPath(relDict,"YOU")
santaPath = getPath(relDict,"SAN")

youOnly = youPath - santaPath
santaOnly = santaPath - youPath

print(len(youOnly) - 1 + len(santaOnly) - 1)