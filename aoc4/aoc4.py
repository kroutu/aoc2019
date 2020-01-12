import os
os.chdir("C:/Users/alexa/Desktop/Python/aoc2019/aoc4")

def decrease(nb):
    strnb = str(nb)
    testing = False
    for t in range(0,len(strnb)-1):
        if int(strnb[t]) > int(strnb[t+1]):
            break
    else:
        testing = True
    return testing

def ddigit(nb):
    strnb = str(nb)
    for t in range(0,len(strnb)-1):
        if int(strnb[t]) == int(strnb[t+1]):
            return True
    return False


def exactlyddigit(nb):
    strnb = str(nb)
    if strnb[0] == strnb[1] and strnb[1] != strnb[2]:
        return True
    if strnb[0] != strnb[1] and strnb[1] == strnb[2] and strnb[2] != strnb[3]:
        return True
    if strnb[1] != strnb[2] and strnb[2] == strnb[3] and strnb[3] != strnb[4]:
        return True
    if strnb[2] != strnb[3] and strnb[3] == strnb[4] and strnb[4] != strnb[5]:
        return True
    if strnb[3] != strnb[4] and strnb[4] == strnb[5]:
        return True
    return False

minPwd = 347312
maxPwd = 805915

counter = 0



for pwd in range(minPwd, maxPwd):
    if exactlyddigit(pwd) and decrease(pwd):
        counter += 1

print(counter)