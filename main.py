from mpl_toolkits.mplot3d import axes3d
import time
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from itertools import combinations
import math as math
from anastruct import SystemElements
import numpy as np


class Node:
    num_of_nodes = 0

    def __init__(self, xpos, ypos, anchor):
        self.xpos = xpos
        self.ypos = ypos
        self.anchor = anchor
        Node.num_of_nodes += 1

    def coords(self):
        return([self.xpos, self.ypos])

    def applyforce(self, force):
        self.force = force


class Truss:
    num_of_truss = 0
    available_mats = 0

    def __init__(self, start, end):
        self.start = start
        self.startx = Nodelist[self.start].xpos
        self.starty = Nodelist[self.start].ypos
        self.end = end
        self.endx = Nodelist[self.end].xpos
        self.endy = Nodelist[self.end].ypos
        self.rise = abs(self.starty - self.endy)
        self.run = abs(self.startx - self.endx)
        Truss.num_of_truss += 1
        Truss.available_mats -= Truss.length(self)

    def tslope(self):
        slope = self.rise/self.run
        return slope

    def tangv(self):
        ang = math.degrees(math.atan(Truss.tslope(self)))
        return ang

    def length(self):
        dist = math.sqrt(self.rise**2 + self.run**2)
        return dist

    def midpoint(self):
        x = (self.startx + self.endx)/2
        y = (self.starty + self.endy)/2
        return (x, y)

############################################################################################################################


def triangleify(coords):
    bars = []
    output = []
    triangles = Delaunay(coords)
    triangles = triangles.simplices
    for row in triangles:
        comb = combinations(row, 2)
        for i in comb:
            bars.append(i)
    for i in bars:
        duplic = i[::-1]
        for j in bars:
            if duplic == j:
                bars.remove(j)
    for i in bars:
        output.append(Truss(i[0], i[1]))
    return output


###########################################################################################################################################


def getnodeid(node):
    id = ss.find_node_id(node.coords())
    return(id)


def addobj(trusslist, Nodelist):
    for i in trusslist:
        ss.add_truss_element(location=[[i.startx, i.starty], [i.endx, i.endy]], EA=8*(10**11))

    for i in range(0, len(Nodelist), 1):
        if Nodelist[i].anchor == 1:
            ss.add_support_fixed(node_id=getnodeid(Nodelist[i]))
        elif Nodelist[i].anchor == 2:
            ss.add_support_roll(node_id=getnodeid(Nodelist[i]), direction=1)


def nodeforce(Nodelist, force):
    for i in range(0, len(Nodelist), 1):
        if Nodelist[i].anchor == 3:
            Nodelist[i].applyforce(force*-1)
            ss.point_load(node_id=getnodeid(Nodelist[i]), Fx=0, Fy=Nodelist[i].force, rotation=0)


def stiffness(force, nodelist):
    for i in range(0, len(nodelist), 1):
        if nodelist[i].anchor == 3:
            newpos = ss.get_node_displacements(node_id=getnodeid(nodelist[i]))
            delx = newpos["ux"]
            dely = newpos["uy"]
            dist = math.sqrt(delx**2 + dely**2)
            # return(force/dist)
            return(dist)

##############################################################################################################


def definenodelist(x, y, nodelist):
    ss = SystemElements()
    nodelist = []
    # Back Wheel (Stationary Mount)
    nodelist.append(Node(0, 0, 1))
    # Front Wheel (Moving Mount)
    nodelist.append(Node(70, 45, 2))
    # Pedal Mount (Normal Node)
    nodelist.append(Node(30, 0, 0))
    # Force Node
    nodelist.append(Node(x, y, 3))
    # Available Material
    Truss.available_mats = 300
    return nodelist


def definecoordlist(nodelist):
    for i in Nodelist:
        coordlist.append(Node.coords(i))
    return(coordlist)


ss = SystemElements()

sval = []
poscoordsx = []
poscoordsy = []
bestcoords = []
currentsmallest = 100
for i in range(20, 40, 1):
    for j in range(1, 100, 1):
        ss = SystemElements()
        Nodelist = []
        Nodelist = definenodelist(i, j, Nodelist)

        coordlist = []
        coordlist = definecoordlist(Nodelist)

        trusslist = []
        trusslist = triangleify(coordlist)
        force = 10000000000
        addobj(trusslist, Nodelist)
        nodeforce(Nodelist, force)
        ss.solve(max_iter=5)
        stiff = stiffness(force, Nodelist)
        if stiff < currentsmallest:
            currentsmallest = stiff
            bestcoords = [i, j]
        sval.append(stiffness(force, Nodelist))
        poscoordsx.append(i)
        poscoordsy.append(j)
    print("prog:  ", str(i/30)+"%")

print(currentsmallest, bestcoords)

ss = SystemElements()
Nodelist = []
Nodelist = definenodelist(bestcoords[0], bestcoords[1], Nodelist)

coordlist = []
coordlist = definecoordlist(Nodelist)

trusslist = []
trusslist = triangleify(coordlist)
force = 10000000000
addobj(trusslist, Nodelist)
nodeforce(Nodelist, force)
ss.solve(max_iter=5)
stiff = stiffness(force, Nodelist)
if stiff < currentsmallest:
    currentsmallest = stiff
    bestcoords = (i, j)
sval.append(stiffness(force, Nodelist))
poscoordsx.append(i)
poscoordsy.append(j)

ss.show_structure()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# load some test data for demonstration and plot a wireframe
# Make data.
X = poscoordsx
Y = poscoordsy
Z = sval
ax.plot_trisurf(X, Y, Z)

# rotate the axes and update
for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.show()
    plt.pause(.001)

"""from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Make data.
X = poscoordsx
Y = poscoordsy
Z = sval
print(X)
print(Y)
print(Z)
# Plot the surface.
ax.plot_trisurf(X, Y, Z)

for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.pause(.001)
"""
