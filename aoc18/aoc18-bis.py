import networkx as nx
import time
import matplotlib.pyplot as plt

def draw(g):
    pos = nx.shell_layout(g)
    nx.draw_networkx(g,pos)

def initGraph():
    donnees = open("test4.txt",'r')
    terrain_brut = donnees.read().splitlines()
    donnees.close()
    base = nx.Graph()
    cases = base.nodes()
    d = {}
    for y,ligne in enumerate(terrain_brut):
        for x,c in enumerate(ligne):
            if c != '#':
                base.add_node((x,y))
                d[c] = (x,y)
    for x,y in cases:
        for adj in (x-1,y),(x+1,y),(x,y-1),(x,y+1):
            if adj in cases:
                base.add_edge((x,y),adj)
    return base, d

def getKey(node):
    for k in d.keys():
        if d[k] == node:
            return k
    return '#'

def getWeights(keys):
    weights = {}
    for k1 in '@'+keys:
        for k2 in keys:
            if k1 != k2 and (k2,k1) not in weights:
                chemin = nx.shortest_path(base,d[k1],d[k2])
                doorList = list(filter(str.isupper,[getKey(k) for k in chemin]))
                weights[(k1,k2)] = len(chemin) - 1, doorList
    return weights

def reachable(start,left,top):
    for key in left:
        if all(d not in left for d in simpl[start][d[key]]['doors']) \
            and simpl[start][d[key]]['weight'] + len(left) < top:
            yield key

def distance(start,end,suppl,left_keys):
    poids = simpl[start][d[end]]['weight']
    return poids + best_path(suppl + poids, d[end], left_keys.replace(end,""))

def best_path(dist, start, remaining_keys):
    global best
    # Fin de récursion
    if len(remaining_keys) == 1:
        if dist + simpl[start][d[remaining_keys]]['weight'] < best:
            best = dist + simpl[start][d[remaining_keys]]['weight']
        return simpl[start][d[remaining_keys]]['weight']
    dists = [distance(start, k, dist, remaining_keys) for k in reachable(start,remaining_keys,best-dist)]
    return min(dists) if dists else best

# Génération du graphe des clés
T0 = time.perf_counter()
base, d = initGraph()
keys = "".join(list(filter(str.islower,d.keys())))
weights = getWeights(keys)
for k1,k2 in weights:
    dist, doors = weights[k1,k2]
    base.add_edge(d[k1],d[k2], weight = dist, doors = "".join(list(doors)).lower())
simpl = nx.subgraph(base,[d[k] for k in '@'+keys])
T1 = time.perf_counter()
print("Temps initialisation :\t",T1-T0)
best = 10**10
print("Partie 1 :\t\t",best_path(0, d['@'], keys))
T2 = time.perf_counter()
print("Temps partie 1 :\t",T2-T1)