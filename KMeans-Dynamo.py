'''
Created by @range-et
this also works as rough K-Means implementation in Dynamo/Grasshopper
remove the libraries that are not required for a Dynamo implementation otherwise it gives an error
import necessary libaries for either environment
Please note : I dont maintain this, I'll be happy to clear up any doubts
Also this was written when I just got into code and it isn't the most optimum implementation
This is a 2d implementation. Please include Z values when implementing this in 3d 
'''
# regular imports
import sys
import random

# IPY stubs remove if not necessary
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\DLLs')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')

# Autodesk specific references, remove if not required
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point

# these are the input variables for the input nodes.
# CHANGE THE LABEL NAMES IF THOSE ARE CHANGED

PointsRaw = IN[0]
NumberOfsubdivisionClasses = IN[1]
iterationNumber = IN[2]

# The Point Class
# Creates a reference for what a point is
# Easier to understand, completely skip-able 
# for faster and cleaner implementation
class Point_2D:
    def __init__(self, Xpos, Ypos, Label):
        self.Xpos = Xpos
        self.Ypos = Ypos
        self.Label = Label
        self.DistanceToCentroid = None

# Creates a reference for what a centroid "K-means point" is
# Easier to understand, completely skip-able 
# for faster and cleaner implementation
# The centroid point Class
class Cent:
    def __init__(self, X, Y, centroidLabel):
        self.X = X
        self.Y = Y
        self.centroidLabel = centroidLabel


# Helper functions

# returns the maximum and minimum in a list
def MinMax(List):

    Lsorted = sorted(List)
    Minimum = Lsorted.pop(0)
    Maximum = Lsorted.pop(-1)

    return(Minimum, Maximum)


# PointDeconstructor
# Convert the point from Autodesk Geometry to the native
# description of what a point is
def DeconstructPoint(point):
    xval = point.X
    yval = point.Y
    pos = (xval, yval)
    return pos


# Hypothenuse calculator
# this exists as a native function under Math use that to optimize
def Hypotcalc(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = (((x2 - x1)**2) + ((y2 - y1)**2))**(0.5)
    return distance

# calculate mean
# also exists as an in-built function
def Calculate_Mean(listOfNumbers):
    summation = 0
    for number in listOfNumbers:
        summation = float(summation) + float(number)

    mean = (float(summation)) / float(len(listOfNumbers))

    return mean

# Subroutine for calculating the centroid Points
# calculates and assigns the points in a point cloud to groups
# in the centroid point list, essentially what happens every iteration in K Means
def CalculateDistance(pointsList, CentroidsList):
    # the new centroid points list
    newPointsList = []

    for point in pointsList:
        # use mathf.infinity, here I used 10^10 to keep it beginner friendly
        shortestDistance = 10**10
        # -1 is out of range as an index value so it does not initialize value
        # here we assign it to one of the cluster groups
        CurrentPointLabel = -1
        # this is the conversion into the scripts geometric idea of a point
        px = point.Xpos
        py = point.Ypos
        pointp = px, py

        # loop through the centroid points and find the closest point
        for centroidindex in range(len(CentroidsList)):
            centroid = CentroidsList[centroidindex]
            cx = centroid.X
            cy = centroid.Y
            pointCent = cx, cy
            distance = Hypotcalc(pointp, pointCent)

            # calculate and set the current lowest distance and the label of the point
            if distance < shortestDistance:
                shortestDistance = distance
                CurrentPointLabel = centroid.centroidLabel


        point.DistanceToCentroid = shortestDistance
        point.Label = CurrentPointLabel
        newPointsList.append(point)

    return newPointsList


# main Function (Core Loop)
def K_means(NumberOfclusters, pointX, pointY, iterations):
    # find the min and max domain of the point clouds that we are working with
    # instanciating a point outside that only increases time to converge at a solution
    minX, maxX = MinMax(pointX)
    minY, maxY = MinMax(pointY)

    # Blank Points Lists
    # this is the list of the point cloud i.e. the data
    pointsForFitting = []
    # the means of the resulting clusters
    centroidPoints = []

    # add all the points in the data point list to be processed
    for i in range(len(pointX)):
        pnt = Point_2D(pointX[i], pointY[i], None)
        pointsForFitting.append(pnt)

    # create and add the randomly instanciated centroid points
    for i in range(NumberOfclusters):
        centroidX = (random.uniform(minX, maxX))
        centroidY = (random.uniform(minY, maxY))
        centroid = Cent(centroidX, centroidY, i)
        centroidPoints.append(centroid)

    # this is the main iteration loop for the K-means process
    for iteration in range(iterations):
        
        FitmentPoint = pointsForFitting
        FitmentPoint = CalculateDistance(FitmentPoint, centroidPoints)

        # final points lists, split by various centroids
        SplitList = []

        for Label in range(NumberOfclusters):
            newList = []
            for point in FitmentPoint:
                if point.Label == Label:
                    newList.append(point)
            SplitList.append(newList)

        
        for centroid in centroidPoints:
            Xs = []
            Ys = []

            Label = centroid.centroidLabel
            ClassIndex = SplitList[Label]
            for point in ClassIndex:
                x = point.Xpos
                y = point.Ypos
                Xs.append(x)
                Ys.append(y)

            X_mean = Calculate_Mean(Xs)
            Y_mean = Calculate_Mean(Ys)

            centroid.X = X_mean
            centroid.Y = Y_mean

        print('Iteration {}'.format(iteration + 1))

    Centroid_X_values = []
    Centroid_Y_values = []

    for centroidPoint in centroidPoints:
        Centroid_X_values.append(centroidPoint.X)
        Centroid_Y_values.append(centroidPoint.Y)

    return (Centroid_X_values, Centroid_Y_values)

# Final loop to run the K means process
pointXs = []
pointYs = []
outputPoints = []
for point in PointsRaw:
    px, py = DeconstructPoint(point)
    pointXs.append(px)
    pointYs.append(py)

CXs, CYs = K_means(NumberOfsubdivisionClasses, pointXs, pointYs, iterationNumber)

for i in range(len(CXs)):
    point = Point.ByCoordinates(CXs[i], CYs[i], 0)
    outputPoints.append(point)
OUT = outputPoints
