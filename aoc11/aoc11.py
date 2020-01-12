import IntComputer as IC
from PIL import Image

# Lecture fichier d'entrée
donnees = open("aoc11.txt",'r')
intlist = list(map(int,donnees.read().split(",")))
donnees.close()

dirs = "URDL"
dx = {"U":lambda x: x,   "D":lambda x: x,   "L":lambda x: x-1, "R":lambda x: x+1}
dy = {"U":lambda y: y-1, "D":lambda y: y+1, "L":lambda y: y,   "R":lambda y: y}

def changePanel(move,direction,panel):
    direction = dirs[dirs.index(direction) - 1] if move == 0 else dirs[(dirs.index(direction) + 1)%4]
    panel = dx[direction](panel[0]),dy[direction](panel[1])
    return panel,direction

currentPanel = 0,0
direction = "U"
panels = {currentPanel:1}

robot = IC.IntComputer(intlist)

while not robot.isOver():
    robot.addInput(panels.setdefault(currentPanel,0))
    robot.operate()
    panels[currentPanel] = robot.getOutput()
    currentPanel,direction = changePanel(robot.getOutput(),direction,currentPanel)

print(len(panels))

xmin, xmax = min(panel[0] for panel in list(panels.keys())), max(panel[0] for panel in list(panels.keys()))
ymin, ymax = min(panel[1] for panel in list(panels.keys())), max(panel[1] for panel in list(panels.keys()))

registration = Image.new("1",(xmax-xmin+1,ymax-ymin+1))
for panel in panels.keys():
    registration.putpixel(panel, panels[panel])
registration.convert("P").resize((xmax*25,ymax*25)).show()
