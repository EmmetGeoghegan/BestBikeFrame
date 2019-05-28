import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from itertools import combinations
import math as math

import pygame as pg
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


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
        self.end = end
        Truss.num_of_truss += 1
        Truss.available_mats -= Truss.length(self)

    def tslope(self):
        rise = math.abs(Nodelist[self.start].ypos - Nodelist[self.end].ypos)
        run = math.abs(Nodelist[self.start].xpos - Nodelist[self.end].xpos)
        slope = rise/run
        return slope

    def tangv(self):
        ang = math.degrees(math.atan(Truss.tslope(self)))
        return ang

    def length(self):
        rise = abs(Nodelist[self.start].ypos - Nodelist[self.end].ypos)
        run = abs(Nodelist[self.start].xpos - Nodelist[self.end].xpos)
        dist = math.sqrt(rise**2 + run**2)
        return dist

    def midpoint(self):
        x = (Nodelist[self.start].xpos + Nodelist[self.end].xpos)/2
        y = (Nodelist[self.start].ypos + Nodelist[self.end].ypos)/2
        return (x, y)


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
        if i.anchor == 1:
            plt.scatter(i.xpos, i.ypos, s=100, color="orange", zorder=2)
        elif i.anchor == 2:
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
# Back Wheel (Stationary Mount)
Nodelist.append(Node(0, 0, 2))
# Pedal Mount (Normal Node)
Nodelist.append(Node(30, 0, 0))
# Front Wheel (Moving Mount)
Nodelist.append(Node(70, 45, 1))
# Mystery Node
Nodelist.append(Node(20, 35, 0))
# Available Material
Truss.available_mats = 300
coordlist = []
for i in Nodelist:
    coordlist.append(Node.coords(i))

trusslist = triangleify(coordlist)

#draw_graph(Nodelist, trusslist)
# print(Truss.available_mats)
###########################################################################################################################################


def offsety(val):
    newcoord = 875-(val*10)
    return newcoord


def offsetx(val):
    newcoord = (val*10)+25
    return newcoord


"""def drawtruss(canvas, color, trusslist):
    for i in trusslist:
        start = (offsetx(Nodelist[i.start].xpos), offsety(Nodelist[i.start].ypos))
        end = (offsetx(Nodelist[i.end].xpos), offsety(Nodelist[i.end].ypos))
        pg.draw.line(canvas, color, start, end, 20)


def drawnode(canvas, nodelist):
    for i in nodelist:
        position = (offsetx(i.xpos), offsety(i.ypos))
        if i.anchor == 1:
            pg.draw.circle(canvas, movenodecolor, position, 20, 0)
        elif i.anchor == 2:
            pg.draw.circle(canvas, fixednodecolor, position, 20, 0)
        else:
            pg.draw.circle(canvas, nodecolor, position, 20, 0)"""


def whiteout(canvas, color):
    canvas.fill(color)


def add_bar(space, pos):
    body = pymunk.Body()
    body.position = Vec2d(pos)
    shape = pymunk.Segment(body, (0, 40), (0, -40), 6)
    shape.mass = 2
    shape.friction = 0.7
    space.add(body, shape)
    return body


white = (255, 255, 255)
trusscolor = (0, 0, 0)
nodecolor = (255, 255, 0)
fixednodecolor = (96, 96, 96)
movenodecolor = (255, 128, 0)

pymunk.pygame_util.positive_y_is_up = False
pygame.init()
space.gravity = (0.0, 900.0)
b1 = add_bar(space, (50, 80))


canvas = pg.display.set_mode((900, 900))
clock = pg.time.Clock()
pg.display.set_caption("Bicycle")
whiteout(canvas, white)
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
"""    drawtruss(canvas, trusscolor, trusslist)
    drawnode(canvas, Nodelist)"""
pg.display.update()
