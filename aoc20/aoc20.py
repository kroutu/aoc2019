import networkx as nx
import time
from itertools import product

IN = -1
OUT = 1
INV = {IN : OUT, OUT : IN}
FICHIER = "aoc20.txt"

def draw(g):
    pos = nx.shell_layout(g)
    nx.draw_networkx(g,pos, node_size = 1, font_size = 7)
    e_labels = {edge : str(g.edges[edge]['weight']) for edge in g.edges()}
    nx.draw_networkx_edge_labels(g, pos, edge_labels = e_labels, font_size = 7)

def adj(x,y):
    return [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]

def findLabel(x,y,char):
    for i,j in [(x-1,y),(x,y-1)]:
        try:
            if terrain[j][i].isalpha():
                warp = terrain[j][i] + char
                x1,y1 = i,j
        except:
            continue
    for i,j in [(x+1,y),(x,y+1)]:
        try:
            if terrain[j][i].isalpha():
                warp = char + terrain[j][i]
                x1,y1 = i,j
        except:
            continue
    todo = adj(x,y)+adj(x1,y1)
    largeur = len(terrain[0])
    for a,b in todo:
        try:
            if terrain[b][a] == '.':
                if a == 2 or b == 2 or a == largeur-3 or b == len(terrain)-3:
                    orientation = OUT
                else:
                    orientation = IN
                return warp, (a,b), orientation
        except:
            continue

def ajouter_noeud(x,y):
    for i,j in adj(x,y):
        if terrain[j][i] == ".":
            plan.add_edge((x,y),(i,j), weight = 1)

def part1():
    g = plan.copy()
    for warp,orientation in warp_dict.keys():
        if warp != "AA" and warp != "ZZ":
            g.add_edge(warp_dict[warp,IN],warp_dict[warp,OUT], weight = 1)
    simpl = nx.subgraph(g,warp_dict.values())
    print("Partie 1 :\t\t", nx.dijkstra_path_length(simpl,warp_dict['AA',OUT], warp_dict['ZZ',OUT]))

def getOrient(node):
    for label,orient in warp_dict:
        if warp_dict[label,orient] == node:
            return orient

def part2():
    simpl = nx.subgraph(plan,warp_dict.values())
    for node in simpl.nodes():
        simpl.nodes[node]['depth'] = dict()
    level = 0
    p2 = 10**10
    explore = [(warp_dict['AA',OUT],OUT,0)] # liste de (noeud, orientation, profondeur)
    distance = [-1]

    while explore:
        suivant = []
        dist_suiv = []
        for (warp,orient,level),dist in zip(explore,distance):
            for node in nx.neighbors(simpl,warp):
                node_orient = getOrient(node)
                if node ==  warp_dict['AA',OUT]:
                    continue
                if level == 0 and node_orient == OUT and node != warp_dict['ZZ',OUT]:
                    continue
                if level < 0 and node == warp_dict['ZZ',OUT]:
                    continue
                dist_next = dist + simpl[warp][node]['weight']+1
                if simpl.nodes[node]['depth'].setdefault(level,10**10) < dist_next:
                    continue
                if node == warp_dict['ZZ',OUT]:
                    if p2 > dist_next:
                        p2 = dist_next
                    continue
                if dist_next < p2:
                    simpl.nodes[node]['depth'][level] = dist_next
                    for ((label,_),n) in warp_dict.items():
                        if n == node:
                            node_next = warp_dict[label,INV[node_orient]]
                            break
                    suivant.append((node_next,INV[node_orient], level + node_orient))
                    dist_suiv.append(dist_next)
        explore, distance = suivant, dist_suiv

    print("Partie 2 :\t\t", p2)


def init():
    for y,ligne in enumerate(terrain):
        for x,char in enumerate(ligne):
            if char in " #":
                continue
            if char.isalpha():
                warp, case, orient = findLabel(x,y,char)
                if (warp,orient) not in warp_dict:
                    warp_dict[warp,orient] = case
                    ajouter_noeud(*case)
                continue
            ajouter_noeud(x,y)
    for c1,c2 in product(warp_dict.values(), repeat = 2):
        if c1 != c2 and c1 not in nx.neighbors(plan,c2):
            try:
                plan.add_edge(c1,c2, weight = nx.dijkstra_path_length(plan,c1,c2))
            except:
                continue

t0 = time.perf_counter()

donnees = open(FICHIER,'r')
terrain = donnees.read().splitlines()
donnees.close()
plan = nx.Graph()
warp_dict = {}
init()
t1 = time.perf_counter()
print("Construction graphe : \t",t1-t0)

part1()
t2 = time.perf_counter()
print("Calcul partie 1 : \t",t2-t1)

part2()
t3 = time.perf_counter()
print("Calcul partie 2 : \t",t3-t2)
