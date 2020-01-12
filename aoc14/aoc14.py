import time
from math import ceil,gcd

def init(fichier):
    # Lecture fichier d'entrée
    donnees = open(fichier, 'r')
    liste_recettes = [item.split(" => ") for item in donnees.read().splitlines()]
    donnees.close()

    # Init intermédiaire
    rec = [[string.split(" ") for string in ing] for ing in [item[0].split(", ") for item in liste_recettes]]
    for item in rec:
        for ing in item:
            ing[0] = int(ing[0])
    sortie, liste_éléments = zip(*[item[1].split(" ") for item in liste_recettes])

    # Init utile
    qtés_sortie = {élément : int(qté) for élément,qté in zip(liste_éléments,sortie)}
    entrées = {OUT : IN for IN,OUT in zip(rec,liste_éléments)}
    liste_éléments += ("ORE",)
    quantités_dispos = dict.fromkeys(liste_éléments, 0)

    return liste_éléments, entrées, qtés_sortie, quantités_dispos

def updateStock(i,ing,qté_attendue):
    suppl = ceil(qté_attendue / qtés_sortie[i]) * ing[0] - quantités_dispos[ing[1]]
    if suppl >= 0:
        quantités_dispos[ing[1]] = 0
    else:
        quantités_dispos[ing[1]] -= ceil(qté_attendue / qtés_sortie[i]) * ing[0]
        suppl = 0
    quantités_dispos[i] = ceil(qté_attendue / qtés_sortie[i])*qtés_sortie[i] - qté_attendue
    return suppl

def produceFuel():
    needed['FUEL'] = 1
    current = 'FUEL'
    while not all(needed[k]==0 for k in needed.keys() if k != 'ORE'):
        for ing in entrées[current]:
            if ing[1] not in needed.keys():
                needed[ing[1]] = 0
            needed[ing[1]] += updateStock(current, ing, needed[current])
        needed[current] = 0
        for ing in needed.keys():
            if ing != 'ORE' and needed[ing] > 0:
                current = ing
                break

def deeper(recette,coef):
    for qté,élément in recette:
        if élément == 'ORE':
                yield qté*coef,'ORE'
        else:
            for ing in entrées[élément]:
                if ing[1] != 'ORE':
                    yield qté*coef*ing[0]//qtés_sortie[élément], ing[1]
                else:
                    yield qté*coef,élément

def dependance(recette):
    for i,(_,dépendant) in enumerate(recette):
        if dépendant != "ORE" and not all([item != check for item in entrées[dépendant] for check in recette]):
            return i, dépendant
    return None, None

def simplifier(recette_temp):
    recette = []
    for item in recette_temp:
        for enCours in recette:
            if enCours[1] == item[1]:
                enCours[0] += item[0]
                break
        else:
            recette.append(item)
    return recette

def eclater(recette):
    coef = 1
    dep_index, dep_elem = dependance(recette)
    while dep_elem != None:
        dep_qté = recette[dep_index][0]
        if dep_qté % qtés_sortie[dep_elem] != 0:
            coefficient = qtés_sortie[dep_elem] // gcd(qtés_sortie[dep_elem], dep_qté)
            coef *= coefficient
            for item in recette:
                item[0] *= coefficient
            dep_qté = recette[dep_index][0]

        recette += [[ing[0]*dep_qté//qtés_sortie[dep_elem],ing[1]] for ing in entrées[dep_elem]]
        recette = simplifier(recette)
        recette.pop(dep_index)
        dep_index, dep_elem = dependance(recette)
    return recette, coef

def prodCycle():
    totalFuel = 1
    recette = [item.copy() for item in entrées['FUEL']]
    next_recette = []

    while recette != next_recette:
        if len(next_recette) > 0:
            recette = [item.copy() for item in next_recette]
        recette, coef = eclater(recette)
        totalFuel *= coef
        coef = 1
        # Calcul du coefficient de cycle
        for ing in recette:
            if ing[0] % qtés_sortie[ing[1]] != 0:
                coef_nec = qtés_sortie[ing[1]] // gcd(ing[0], qtés_sortie[ing[1]])
                coef *= coef_nec // gcd(coef, coef_nec)
        # Génération du niveau suivant avec application du coef
        totalFuel *= coef
        next_recette = simplifier([list(ing) for ing in deeper(recette,coef)])
    ore = sum(entrées[char][0][0]*qté // qtés_sortie[char] for qté,char in recette)
    return ore, totalFuel

t0 = time.perf_counter()
liste_éléments, entrées, qtés_sortie, quantités_dispos = init("aoc14.txt")

needed = {}

produceFuel()

t1 = time.perf_counter()
print("Temps d\'initialisation :",t1-t0)
del t0

print("Part1 :\t", needed['ORE'])
t2 = time.perf_counter()
print("Temps de partie 1 :\t", t2-t1)
del t1

ore_cycle, totalFuel = prodCycle()
shortCycle = False

if ore_cycle > 1000000000000:
    print("Cycle trop long !")
    shortCycle = True
    totalFuel = 1
    while totalFuel < 10000:
        produceFuel()
        totalFuel += 1
    ore_cycle = needed['ORE']

cycles = 1000000000000 // ore_cycle
needed['ORE'] = ore_cycle * cycles
totalFuel *= cycles
if shortCycle:
    for item in liste_éléments:
        quantités_dispos[item] *= cycles

while needed['ORE'] <= 1000000000000:
    produceFuel()
    totalFuel += 1

print("Part2 :\t", totalFuel-1)
print("Temps de partie 2 :\t", time.perf_counter()-t2)
del t2