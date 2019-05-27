import matplotlib.pyplot as plt
import random
from scipy.spatial import Delaunay
from itertools import permutations


class Node:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.coords = [xpos, ypos]


class Truss:
    pass


class Graph:
    pass


node_1 = Node(5, 6)
node_2 = Node(5, 6)


print(node_1.xpos)


"""
def triangleify(hingelist):
    triangles = Delaunay(hingelist)
    triangles = triangles.simplices
    for row in triangles:
        perm = permutations(row, 2)
        for i in perm:
            add_truss(i[0], i[1])


def add_truss(pt1, pt2):
    trusslist.append([pt1, pt2])


def add_hinge(x, y):
    hingelist.append([x, y])


def draw_graph(hingelist, trusslist):
    # Unzip and get our x and y co-ords
    xpts, ypts = zip(*hingelist)
    # Draw Trusses
    for i in trusslist:
        start = i[0]
        end = i[1]
        plt.plot([xpts[start], xpts[end]], [ypts[start], ypts[end]], color="blue", linewidth=2, zorder=1)
    # Draw Hinges
    plt.scatter(xpts, ypts, s=100, color="blue", zorder=2)
    # Draw Hinge labels
    for i in range(0, len(hingelist), 1):
        plt.annotate(i, (hingelist[i][0], hingelist[i][1]), size=20, color="black", zorder=3)
    plt.title("Our Structure")
    plt.xlabel("x-Coords")
    plt.ylabel("y-Coords")
    plt.show()


def main():
    draw_graph(hingelist, trusslist)


hingelist = []
trusslist = []


for i in range(0, 5):
    add_hinge(random.randint(-10, 10), random.randint(-10, 10))
triangleify(hingelist)
main()
"""
