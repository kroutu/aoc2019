import time
TX = time.perf_counter()

import networkx as nx

def draw(g):
    pos = nx.spring_layout(g)
    n_labels = {(node,*rest) : "".join(list(node)) for node,*rest in g.nodes()}
    nx.draw_networkx(g,pos, node_size = 1, arrowsize = 5, labels = n_labels, font_size = 7)
    e_labels = {edge : str(g.edges[edge]['weight']) for edge in g.edges()}
    nx.draw_networkx_edge_labels(g, pos, edge_labels = e_labels, font_size = 7)

def initGraph(partie):
    def getKey(node):
        nonlocal d
        for k in d.keys():
            if d[k] == node:
                return k
        return '#'

    def getWeights(keys):
        nonlocal base
        weights = {}
        for k in keys:
            for i in range(4):
                try:
                    chemin = nx.shortest_path(base,d['@'+str(i)],d[k])
                    doorList = list(filter(str.isalpha,[getKey(k) for k in chemin[1:len(chemin)-1]]))
                    weights[('@'+str(i),k)] = len(chemin) - 1, doorList
                except KeyError:
                    break
                except nx.NetworkXNoPath:
                    continue
        for k1 in keys:
            for k2 in keys:
                if k1 != k2 and (k2,k1) not in weights:
                    try:
                        chemin = nx.shortest_path(base,d[k1],d[k2])
                        weights[(k1,k2)] = len(chemin) - 1, ""
                    except nx.NetworkXNoPath:
                        continue
        return weights

    def initSetLastGraph():
        nonlocal simpl, weights, keys, keys_s
        state = nx.DiGraph()
        for i in range(4):
            try:
                for k in nx.neighbors(simpl,d['@'+str(i)]):
                    if not simpl.nodes[k]['doors']:
                        mem = ['@'+str(i) for i in range(4)]
                        mem[i] = getKey(k)
                        state.add_edge((frozenset("@"),),(frozenset(getKey(k)),tuple(mem)),weight = weights['@'+str(i),getKey(k)][0])
            except KeyError:
                break

        for i in range(1,len(keys)):
            todo = list(filter(lambda x:x[0]!=frozenset("@") and len(x[0])==i,state.nodes()))
            for s,last in todo:
                for k in keys_s-s:
                    if all(r in s for r in simpl.nodes[d[k]].setdefault('doors',"")):
                        for j in range(4):
                            try:
                                dist = weights[k,last[j]][0] if (k,last[j]) in weights else weights[last[j],k][0]
                                mem = list(last)
                                mem[j] = k
                                next_node = (keys_s,) if i == len(keys)-1 else (s|frozenset(k),tuple(mem))
                                state.add_edge((s,last), next_node, weight = dist)
                                break
                            except KeyError:
                                continue
        return state

    donnees = open("aoc18-{}.txt".format(partie),'r')
    #donnees = open("test1.txt",'r')
    terrain_brut = donnees.read().splitlines()
    donnees.close()
    base = nx.Graph()
    cases = base.nodes()
    d = {}
    robot = 0
    for y,ligne in enumerate(terrain_brut):
        for x,c in enumerate(ligne):
            if c != '#':
                base.add_node((x,y))
                if c == '@':
                    c += str(robot)
                    robot += 1
                d[c] = (x,y)
    for x,y in cases:
        for adj in (x-1,y),(x+1,y),(x,y-1),(x,y+1):
            if adj in cases:
                base.add_edge((x,y),adj)

    # Génération du graphe des clés
    T0 = time.perf_counter()
    keys = "".join(list(filter(str.islower,d.keys())))
    keys_s = frozenset(list(keys))
    T1 = time.perf_counter()
    print("Temps graphe complet :\t",T1-T0)

    # Graphe avec seulement les clés
    weights = getWeights(keys)
    for k1,k2 in weights:
        dist, doors = weights[k1,k2]
        if k1[0] == '@':
            base.nodes[d[k2]]['doors'] = "".join(list(doors)).lower()
        base.add_edge(d[k1],d[k2], weight = dist)
    simpl = nx.subgraph(base,[d[k] for k in ['@'+str(i) for i in range(robot)]+list(keys)])
    T2 = time.perf_counter()
    print("Temps graphe clés :\t",T2-T1)
    state = initSetLastGraph()
    T3 = time.perf_counter()
    print("Temps graphe état :\t",T3-T2)
    return state, keys_s

def part1():
    state, keys_s = initGraph(1)
    #draw(state)
    T3 = time.perf_counter()
    print("Partie 1 : \t", nx.dijkstra_path_length(state,(frozenset("@"),),(keys_s,)))
    T4 = time.perf_counter()
    print("Temps calcul chemin :\t",T4-T3)

def part2():
    state, keys_s = initGraph(2)
    T3 = time.perf_counter()
    print("Partie 2 : \t", nx.dijkstra_path_length(state,(frozenset("@"),),(keys_s,)))
    T4 = time.perf_counter()
    print("Temps calcul chemin :\t",T4-T3)

TA = time.perf_counter()
print("Import NetworkX :\t",TA-TX)
part1()
part2()
TB = time.perf_counter()
print("Temps total :\t",TB-TA)