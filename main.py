import matplotlib.pyplot as plt


def draw_graph(xpts, ypts, trusslist):
    plt.scatter(xpts, ypts, s=100, color="blue")
    for i in range(0, len(xpts), 1):
        plt.annotate(i, (xpts[i], ypts[i]), size=20, color="black")
    plt.title("Our Structure")
    plt.xlabel("x-Coords")
    plt.ylabel("y-Coords")
    for i in trusslist:
        start = i[0]
        end = i[1]
        plt.plot([xpts[start], xpts[end]], [ypts[start], ypts[end]], color="blue", linewidth=2)
    plt.show()


def add_hinge(x, y):
    xpts.append(x)
    ypts.append(y)


def add_truss(pt1, pt2):
    trusslist.append([pt1, pt2])


xpts = []
ypts = []
trusslist = []

add_hinge(5, 5)
add_hinge(6, 6)
add_hinge(-10, 6)

add_truss(0, 1)
add_truss(0, 2)
draw_graph(xpts, ypts, trusslist)
