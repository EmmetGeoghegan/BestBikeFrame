import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from itertools import combinations
import math as math
from anastruct import SystemElements


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


Nodelist = []
# Back Wheel (Stationary Mount)
Nodelist.append(Node(0, 0, 1))
# Front Wheel (Moving Mount)
Nodelist.append(Node(70, 45, 2))
# Pedal Mount (Normal Node)
Nodelist.append(Node(30, 0, 0))
# Force Node
Nodelist.append(Node(20, 35, 3))
# Available Material
Truss.available_mats = 300
coordlist = []
for i in Nodelist:
    coordlist.append(Node.coords(i))

trusslist = triangleify(coordlist)

###########################################################################################################################################

ss = SystemElements()


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
            print("dist", dist)
            # return(force/dist)
            return(dist)


addobj(trusslist, Nodelist)
force = 10000000000
nodeforce(Nodelist, force)
ss.solve(max_iter=500)

print(stiffness(force, Nodelist), "is the stiffness for the current sys")


ss.show_displacement(factor=50)
