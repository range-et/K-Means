'''
Created by @range-et
this also works as rough K-Means implementation in Dynamo/Grasshopper
import necessary libaries for either environment (here, the imports are for rhino)
Please note : I dont maintain this, I'll be happy to clear up any doubts
Also this was written when I just got into code and it isn't the most optimum implementation
This is a 2d implementation. Please include Z values when implementing this in 3d 

    Provides a scripting component.
    Inputs:
        points: The points script variable
        clusters: The the number of clusters script variable
        iterations: The the number of iterations script variable
    Output:
        a: The a output variable
'''

__author__ = "range"
__version__ = "2019.07.14"

# regular imports
import rhinoscriptsyntax as rs
import random 

# these are the inputs of the python node
# PLEASE CHANGE THE INPUT NAMES
PointsRaw = points
NumberOfsubdivisionClasses = int(clusters)
iterationNumber = int(iterations)

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
def DeconstructPoint(pCords):
    point = rs.PointCoordinates(pCords)
    xval = point.X
    yval = point.Y
    pos = (xval, yval)
    return pos


# Hypothenuse calculator
def Hypotcalc(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = (((x2 - x1)**2) + ((y2 - y1)**2))**(0.5)
    return distance


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


# calculate mean
def Calculate_Mean(listOfNumbers):
    summation = 0
    for number in listOfNumbers:
        summation = float(summation) + float(number)

    mean = (float(summation)) / float(len(listOfNumbers))

    return mean


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

# Final loop
pointXs = []
pointYs = []
outputPoints = []
for point in PointsRaw:
    px, py = DeconstructPoint(point)
    pointXs.append(px)
    pointYs.append(py)

CXs, CYs = K_means(NumberOfsubdivisionClasses, pointXs, pointYs, iterationNumber)

for i in range(len(CXs)):
    point = rs.CreatePoint(CXs[i], CYs[i], 0)
    outputPoints.append(point)
a = outputPoints
