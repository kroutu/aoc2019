import time
from math import ceil

def init():
    donnees = open("aoc16.txt", 'r')
    seq = [int(c) for c in donnees.read()]
    donnees.close()
    return seq

def getRes(seq):
    return sum(elem * (10**i) for i,elem in enumerate(reversed(seq)))

def process2(seq,offset = 0):
    taille = len(seq)
    next_seq = []
    if offset != 0:
        next_seq = [0]*offset
    for i in range(offset,ceil((taille-2)/3)):
        inter = i+1
        somme = 0
        for j in range(i,taille,4*inter):
            fin = min(taille, j+inter)
            somme += sum(seq[j:fin])
            fin = min(taille,j + 3*inter)
            somme -= sum(seq[j+2*inter:fin])
        next_seq.append(abs(somme)%10 if somme < 0 else somme%10)
    else:
        try:
            next_seq.append(sum(seq[i+1:i+inter+2])%10)
        except:
            i = offset - 1
            inter = i + 1
            next_seq.append(sum(seq[i+1:i+inter+2])%10)
        for j in range(i+2,taille-1):
            next_seq.append(abs(10+next_seq[-1]-seq[j-1]+sum(seq[2*j-1:2*j+1]))%10)
    next_seq.append(seq[-1])
    return next_seq

def part1():
    t0 = time.perf_counter()
    seq = init()
    it = 0
    while it < 100:
        it += 1
        seq = process2(seq)
    print("Partie 1 :\t\t",getRes(seq[:8]))
    t1 = time.perf_counter()
    print("Temps partie 1 :\t",t1-t0)

def part2():
    t0 = time.perf_counter()
    seq = init()*10000
    offset = sum(elem * 10**i for i,elem in enumerate(reversed(seq[:7])))
    it = 0
    while it < 100:
        it += 1
        seq = process2(seq,offset)
    print("Partie 2 :\t\t",getRes(seq[offset:offset+8]))
    t1 = time.perf_counter()
    print("Temps partie 2 :\t",t1-t0)

part1()
part2()