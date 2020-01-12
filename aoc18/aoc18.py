import networkx as nx
import time

def initGraph():
    donnees = open("test5.txt",'r')
    terrain_brut = donnees.read().splitlines()
    donnees.close()
    base = nx.Graph()
    cases = base.nodes()
    d = {}
    for y,ligne in enumerate(terrain_brut):
        for x,c in enumerate(ligne):
            if c != '#':
                base.add_node((x,y), door = c.isupper())
                d[c] = (x,y)
    for x,y in cases:
        if cases[(x,y)]['door']:
            continue
        for adj in (x-1,y),(x+1,y),(x,y-1),(x,y+1):
            if adj in cases and not cases[adj]['door']:
                base.add_edge((x,y),adj)
    return base, d

def openDoor(k):
    door = chr(ord(k)-32)
    if door in d.keys():
        x,y = d[door]
        for adj in (x-1,y),(x+1,y),(x,y-1),(x,y+1):
            if adj in base.nodes():
                base.add_edge(d[door],adj)

def closeDoor(k):
    door = chr(ord(k)-32)
    if door in d.keys():
            x,y = d[door]
            for adj in (x-1,y),(x+1,y),(x,y-1),(x,y+1):
                if adj in nx.neighbors(base,d[door]):
                    base.remove_edge(d[door],adj)

def path(dist_parcourue,keylist,start, best = 10**10):
    # Fin récursion = dernière clé
    if len(keylist) == 1:
        return nx.shortest_path_length(base,start,d[keylist])
    # Recherche des clés accessibles (hors déjà trop long et clé sur le chemin)
    candidates = {}
    for key in keylist:
        try:
            chemin = nx.shortest_path(base,start,d[key])
            distance = len(chemin)-1
            if distance + dist_parcourue + len(keylist) <= best and all(d[k] not in chemin[:distance] for k in keylist):
                candidates[key] = distance
        except nx.NetworkXNoPath:
            continue
    # Cul-de-sac
    if len(candidates.keys())==0:
        return best
    # Récursion
    dists = []
    result = best
    for key in candidates.keys():
        dist_next = dist_parcourue + candidates[key]
        openDoor(key)
        dists.append(candidates[key] + path(dist_next,keylist.replace(key,""),d[key],best))
        closeDoor(key)
        if dists[-1] - candidates[key] + dist_next < best:
            best = dists[-1]-candidates[key] + dist_next
            result = dists[-1]
    return result

def getKey(node):
    for k in d.keys():
        if d[k] == node:
            return k
    return '#'

T0 = time.perf_counter()
base, d = initGraph()
keys = "".join(list(filter(str.islower,d.keys())))

print("Partie 1 :\t\t",path(0,keys,d['@']))
T1 = time.perf_counter()
print("Temps partie 1 :\t",T1-T0)