'''
Created by @range-et
This is a visual representation of whats happening in K-Means natively in python
Please note : I dont maintain this, I'll be happy to clear up any doubts
Also this was written when I just got into code and it isn't the most optimum implementation
This is a 2d implementation. Please include Z values when implementing this in 3d 
'''
# regular imports
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import style
style.use('ggplot')

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


# Hypothenuse calculator
def Hypotcalc(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = (((x2 - x1)**2) + ((y2 - y1)**2))**(0.5)
    return distance


# calculate mean
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


# Get a bunch of random points
numberOfpoints = 100
# use numby to get these points
Xvalues = np.ndarray.tolist(np.random.randint(low=-521, high=200, size=numberOfpoints))
Yvalues = np.ndarray.tolist(np.random.randint(low=-120, high=400, size=numberOfpoints))

# final loop to call and process all the points that we initailized
plt.scatter(Xvalues, Yvalues)
CXs, CYs = K_means(4, Xvalues, Yvalues, 50)
plt.scatter(CXs, CYs, c='g')
plt.show()
