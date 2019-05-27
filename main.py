import matplotlib.pyplot as plt
import random
from scipy.spatial import Delaunay


def draw_graph(hingelist, trusslist):
    # Unzip and get our x and y co-ords
    xpts, ypts = zip(*hingelist)
    # Draw Trusses
    triangles = Delaunay(hingelist)
    for i in range(0, len(hingelist), 1):
        plt.triplot(xpts, ypts, triangles.simplices.copy(), zorder=1, color="green")
    # Draw Hinges
    plt.scatter(xpts, ypts, s=100, color="blue", zorder=2)
    # Draw Hinge labels
    for i in range(0, len(hingelist), 1):
        plt.annotate(i, (hingelist[i][0], hingelist[i][1]), size=20, color="black", zorder=3)
    plt.title("Our Structure")
    plt.xlabel("x-Coords")
    plt.ylabel("y-Coords")
    plt.show()


def add_hinge(x, y):
    hingelist.append([x, y])


def add_truss(pt1, pt2):
    trusslist.append([pt1, pt2])


def main():
    for i in range(0, 5):
        add_hinge(random.randint(-10, 10), random.randint(-10, 10))
    draw_graph(hingelist, trusslist)


hingelist = []
trusslist = []

while True:
    main()
    hingelist = []
    trusslist = []
