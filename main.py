import matplotlib.pyplot as plt
import random
from scipy.spatial import Delaunay
from itertools import combinations
import math as math


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
    available_mats =

    def __init__(self, start, end):
        self.start = start
        self.end = end
        Truss.num_of_truss += 1

    def tslope(self):
        rise = math.abs(Nodelist[self.start].ypos - Nodelist[self.end].ypos)
        run = math.abs(Nodelist[self.start].xpos - Nodelist[self.end].xpos)
        slope = rise/run
        return slope

    def tangv(self):
        ang = math.degrees(math.atan(tslope(self)))
        return ang

    def length(self):
        rise = math.abs(Nodelist[self.start].ypos - Nodelist[self.end].ypos)
        run = math.abs(Nodelist[self.start].xpos - Nodelist[self.end].xpos)
        dist = math.sqrt(rise**2 + run**2)
        return dist


def triangleify(coords):
    j = []
    triangles = Delaunay(coords)
    triangles = triangles.simplices
    for row in triangles:
        comb = combinations(row, 2)
        for i in comb:
            j.append(Truss(i[0], i[1]))
    return j


def draw_graph(nodelist, trusslist):
    # Draw Hinges
    for i in nodelist:
        if i.anchor is 1:
            plt.scatter(i.xpos, i.ypos, s=100, color="orange", zorder=2)
        elif i.anchor is 2:
            plt.scatter(i.xpos, i.ypos, s=100, color="grey", zorder=2)
        else:
            plt.scatter(i.xpos, i.ypos, s=100, color="cyan", zorder=2)

    # Draw Trusses
    for i in trusslist:
        plt.plot((nodelist[i.start].xpos, nodelist[i.end].xpos), (nodelist[i.start].ypos,
                                                                  nodelist[i.end].ypos), color="cyan", linewidth=2, zorder=1)
    plt.plot(1, 2, 6, 9, color="cyan")
    # Draw Hinge labels
    for i in range(0, Node.num_of_nodes, 1):
        plt.annotate(i, (nodelist[i].xpos, nodelist[i].ypos), size=20, color="black", zorder=3)
    plt.title("Our Structure")
    plt.xlabel("x-Coords")
    plt.ylabel("y-Coords")
    plt.show()


Nodelist = []
for i in range(0, 5, 1):
    Nodelist.append(Node(random.randint(1, 10), random.randint(1, 10), random.randint(0, 2)))

coordlist = []
for i in Nodelist:
    coordlist.append(Node.coords(i))

trusslist = triangleify(coordlist)

draw_graph(Nodelist, trusslist)
