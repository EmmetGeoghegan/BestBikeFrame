import plotwithgpu as gpuplot
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from itertools import combinations
import math as math
from anastruct import SystemElements
from os import system
import plotwithgpu as gpuplot  # GPU accelerated rendering Comment if you dont have an Nvida GPU
from tqdm import tqdm


class Node:        # Class to create our nodes and give them properties
    num_of_nodes = 0

    def __init__(self, xpos, ypos, anchor):
        self.xpos = xpos
        self.ypos = ypos
        self.anchor = anchor
        Node.num_of_nodes += 1

    # Gets the coords of  a node
    def coords(self):
        return([self.xpos, self.ypos])

    # Applies a force to a given node
    def applyforce(self, force):
        self.force = force


class Truss:     # Class that creates Trusses and gives them properites
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

    # Gets the slope of a Truss
    def tslope(self):
        slope = self.rise/self.run
        return slope

    # Gets the angle to the vertical of the Truss
    def tangv(self):
        ang = math.degrees(math.atan(Truss.tslope(self)))
        return ang

    # Gets the length of the truss
    def length(self):
        dist = math.sqrt(self.rise**2 + self.run**2)
        return dist

    # Gets the midpoint of the truss
    def midpoint(self):
        x = (self.startx + self.endx)/2
        y = (self.starty + self.endy)/2
        return (x, y)

####################
# Truss Generation #
####################

# This function creates our Truss start and end points by
# Forming Delaunay triangles. The start and end points for each edge
# Are passed to the Truss class to generate our objects


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

########################
# Structure Simulation #
########################


# Function gets the anastruct node ID's of a given node in the model
def getnodeid(node):
    id = ss.find_node_id(node.coords())
    return(id)


# Function to add Trusses and the fixed and rolling supports to the model
def addobj(trusslist, Nodelist):
    for i in trusslist:
        ss.add_truss_element(location=[[i.startx, i.starty], [i.endx, i.endy]], EA=8*(10**11))

    for i in range(0, len(Nodelist), 1):
        if Nodelist[i].anchor == 1:
            ss.add_support_fixed(node_id=getnodeid(Nodelist[i]))
        elif Nodelist[i].anchor == 2:
            ss.add_support_roll(node_id=getnodeid(Nodelist[i]), direction=1)


# Function to add a force to the force node (anchor type 3)
def nodeforce(Nodelist, force):
    for i in range(0, len(Nodelist), 1):
        if Nodelist[i].anchor == 3:
            Nodelist[i].applyforce(force*-1)
            ss.point_load(node_id=getnodeid(Nodelist[i]), Fx=0, Fy=Nodelist[i].force, rotation=0)


# Our Fitness Function, Determines the score of the force nodes location
def stiffness(force, nodelist):
    for i in range(0, len(nodelist), 1):
        if nodelist[i].anchor == 3:
            newpos = ss.get_node_displacements(node_id=getnodeid(nodelist[i]))
            delx = newpos["ux"]
            dely = newpos["uy"]
            dist = math.sqrt(delx**2 + dely**2)
            return(dist)


# Function that defines our nodes. Takes paramaters to place the force node (x,y)
def definenodelist(x, y, nodelist):
    nodelist = []
    # Back Wheel (Stationary Mount)
    nodelist.append(Node(0, 0, 1))
    # Front Wheel (Moving Mount)
    nodelist.append(Node(70, 45, 2))
    # Pedal Mount (Normal Node)
    nodelist.append(Node(30, 0, 3))
    # Force Node
    nodelist.append(Node(x, y, 0))
    # Available Material
    Truss.available_mats = 90.2
    return nodelist


# Function that preps the list of all node co-ordinates to be turned into truss start and end points
def definecoordlist(nodelist):
    for i in Nodelist:
        coordlist.append(Node.coords(i))
    return(coordlist)


###################
# Node Generation #
###################
sval = []
poscoordsx = []
poscoordsy = []
bestcoords = []
currentsmallest = 100
# for i in range(20, 40, 1):
#     for j in range(1, 100, 1):

for i in tqdm(range(20, 40, 1)):
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
    # print("Progress:  ", str(int(((i-20)/19)*100))+"%")
print("Done")
print("Stiffness of the structure: ", currentsmallest)
print("Co-Ordinates:", bestcoords)

################################
# Graphical Physics Simulation #
################################
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
ss.solve(max_iter=50)
ss.show_structure()

###########################
# Plot Values Graphically #
###########################
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X = poscoordsx
Y = poscoordsy
Z = sval
ax.plot_trisurf(X, Y, Z, cmap="jet")
plt.show()


########################
# Plot Values With GPU #
########################
gpuplot.plsplotgpu(Z)
