import matplotlib.pyplot as plt
import random
from scipy.spatial import Delaunay


def draw_graph(xpts, ypts, trusslist):
    # Draw Trusses
    for i in trusslist:
        start = i[0]
        end = i[1]
        plt.plot([xpts[start], xpts[end]], [ypts[start], ypts[end]], color="blue", linewidth=2, zorder=1)
    # Draw Hinges
    plt.scatter(xpts, ypts, s=100, color="blue")
    plt.scatter(xpts[0], ypts[0], s=100, color="red", zorder=2)
    plt.scatter(xpts[-1], ypts[-1], s=100, color="red", zorder=2)
    # Draw Hinge labels
    for i in range(0, len(xpts), 1):
        plt.annotate(i, (xpts[i], ypts[i]), size=20, color="black", zorder=3)
    plt.title("Our Structure")
    plt.xlabel("x-Coords")
    plt.ylabel("y-Coords")
    plt.show()


def add_hinge(x, y):
    xpts.append(x)
    ypts.append(y)


def add_truss(pt1, pt2):
    trusslist.append([pt1, pt2])


xpts = []
ypts = []
trusslist = []

for i in range(0, 5):
    add_hinge(random.randint(-10, 10), random.randint(-10, 10))


"""add_hinge(-10, -5)
add_hinge(-4, 5)
add_hinge(4, -5)
add_hinge(10, 7)

add_truss(0, 1)
add_truss(0, 2)
add_truss(1, 2)
add_truss(3, 2)
add_truss(1, 3)
"""
draw_graph(xpts, ypts, trusslist)
