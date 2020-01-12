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
    for k in keys:
        chemin = nx.shortest_path(base,d['@'],d[k])
        doorList = list(filter(str.isalpha,[getKey(k) for k in chemin[1:len(chemin)-1]]))
        weights[('@',k)] = len(chemin) - 1, doorList
    for k1 in keys:
        for k2 in keys:
            if k1 != k2 and (k2,k1) not in weights:
                chemin = nx.shortest_path(base,d[k1],d[k2])
                weights[(k1,k2)] = len(chemin) - 1, ""
    return weights

def possiblePaths(chemin="",val = 0):
    global best
    for c in keys:
        if c in chemin or not all(r in chemin for r in base.nodes[d[c]].setdefault('doors',"")):
            continue
        temp_val = simpl[d[chemin[-1]]][d[c]]['weight'] if chemin else simpl[d['@']][d[c]]['weight']
        val += temp_val
        distmin = min(simpl[d[c]][node]['weight'] for node in nx.neighbors(simpl,d[c]) if getKey(node) not in chemin)
        if val + len(keys) - distmin*(len(chemin) + 1) < best:
            if len(chemin) == len(keys)-1:
                if val < best:
                    best = val
                    yield chemin + c
            else:
                for suite in possiblePaths(chemin+c,val):
                    yield suite
        val -= temp_val

# Génération du graphe des clés
T0 = time.perf_counter()
base, d = initGraph()
keys = "".join(list(filter(str.islower,d.keys())))
print(nx.is_tree(base))
weights = getWeights(keys)
for k1,k2 in weights:
    dist, doors = weights[k1,k2]
    if k1 == '@':
        base.nodes[d[k2]]['doors'] = "".join(list(doors)).lower()
    base.add_edge(d[k1],d[k2], weight = dist)
simpl = nx.subgraph(base,[d[k] for k in '@'+keys])
T1 = time.perf_counter()
print("Temps initialisation :\t",T1-T0)

best = 10**10
a = possiblePaths()
print(len(list(a)), best)

#print("Partie 1 :\t\t",best_path(0, d['@'], keys))
T2 = time.perf_counter()
print("Temps partie 1 :\t",T2-T1)