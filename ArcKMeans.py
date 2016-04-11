# Import necessary modules
import sys, os, string, math, arcpy, traceback
import numpy as np
import scipy
from copy import copy

# Allow output file to overwrite any existing file of the same name
arcpy.env.overwriteOutput = True

try:
    # Request user input of data type = Shapefile and direction = Input
    nameOfInputShapefile = arcpy.GetParameterAsText(0)

    # Request user input of data type = Shapefile and direction = Output
    nameOfOutputShapefile = arcpy.GetParameterAsText(1)

    # Request user input of data type
    nameOfField1 = arcpy.GetParameterAsText(2)
    nameOfField2 = arcpy.GetParameterAsText(3)
    numberOfClusters = arcpy.GetParameterAsText(4)

     # Get data from fields
    x = []
    rows = arcpy.SearchCursor(nameOfInputShapefile,[nameOfField1])
    for r in rows:
        x.append(r.getValue(nameOfField1))

    y = []
    rows = arcpy.SearchCursor(nameOfInputShapefile,[nameOfField2])
    for r in rows:
        y.append(r.getValue(nameOfField2))

    dataSet = []
##    z = zip(x,y)
    for i in range (0,len(x)):
        dataSet.append([float(x[i]), float(y[i])])
    arcpy.AddMessage(len(dataSet))

    from numpy import *
    import time
    import matplotlib.pyplot as plt
    from copy import copy

    # calculate Euclidean distance
    def euclDistance(vector1, vector2):
        return sqrt(sum(power(vector2 - vector1, 2)))

    # init centroids with random samples
    def initCentroids(dataSet, k):
        numSamples, dim = dataSet.shape
        centroids = zeros((k, dim))
        for i in range(k):
            index = int(random.uniform(0, numSamples))
            centroids[i, :] = dataSet[index, :]
        return centroids

    # k-means cluster
    def kmeans(dataSet, k):
        numSamples = dataSet.shape[0]
        # first column stores which cluster this sample belongs to,
        # second column stores the error between this sample and its centroid
        clusterAssment = mat(zeros((numSamples, 2)))
        clusterChanged = True

        ## step 1: init centroids
        centroids = initCentroids(dataSet, k)

        while clusterChanged:
            clusterChanged = False
            ## for each sample
            for i in xrange(numSamples):
                minDist  = 100000.0
                minIndex = 0
                ## for each centroid
                ## step 2: find the centroid who is closest
                for j in range(k):
                    distance = euclDistance(centroids[j, :], dataSet[i, :])
                    if distance < minDist:
                        minDist  = distance
                        minIndex = j

                ## step 3: update its cluster
                if clusterAssment[i, 0] != minIndex:
                    clusterChanged = True
                    clusterAssment[i, :] = minIndex, minDist**2

            ## step 4: update centroids
            for j in range(k):
                pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
                centroids[j, :] = mean(pointsInCluster, axis = 0)

        print 'Congratulations, cluster complete!'
        return centroids, clusterAssment

    ## step 2: clustering...
    print "step 2: clustering..."
    dataSet = mat(dataSet)
    k = int(numberOfClusters)
    centroids, clusterAssment = kmeans(dataSet, k)
    clust = []
    for i in range(0,len(clusterAssment)):
        clust.append(clusterAssment[i,0])
    arcpy.AddMessage(clust)
    arcpy.AddMessage(len(clust))

    # Replicate the input shapefile and add a new field to the replica
    arcpy.Copy_management(nameOfInputShapefile, nameOfOutputShapefile)
    arcpy.AddField_management(nameOfOutputShapefile, "km", "DOUBLE")

    # add values to the new field
    cur = arcpy.UpdateCursor(nameOfOutputShapefile)
    j = 0
    for row in cur:
        value = clust[j]
        row.setValue('km',value)
        cur.updateRow(row)
        j = j+1

    del row
    del cur


except Exception as e:
    # If unsuccessful, end gracefully by indicating why
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    # ... and where
    exceptionreport = sys.exc_info()[2]
    fullermessage   = traceback.format_tb(exceptionreport)[0]
    arcpy.AddError("at this location: \n\n" + fullermessage + "\n")

