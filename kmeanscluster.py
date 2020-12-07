import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D



def euclideanDistance (point1, point2):
    distance = 0

    #each point has 2 or 3 dimensions (depending on PCA), but they should be the same size
    #just calculate the euclidean distance
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2

    return math.sqrt(distance)

def importData (csvFile):

    #import as panda DF
    DFData = pd.read_csv(csvFile)
    DFData.rename(columns = {'Unnamed: 0':'Sample'}, inplace = True)

    #change to numpy array (easier for me to work with)
    NPData = DFData.values


    return DFData, NPData


#getting the min and max of each column (PCA), and returning as a list of list
#i.e. [[1, 3] , [4, 9], [3, 7]] for 3 PCA
def minMax(Data):
    minMaxDF = Data.agg([min, max])
    list = []
    for i in range(1, len(minMaxDF.columns)):

        list.append([minMaxDF.iloc[0][i], minMaxDF.iloc[1][i]])

    return list


class KMeans:
    def __init__(self, k, tolerance, maxIters):
        self.k = k
        self.tolerance = tolerance
        self.maxIters = maxIters
        self.centroids = {} #dictionary of centroids ie centroid1: [1, 2, 3]
        self.clusters = {} #dictionary of clusters, ie  cluster1: [[gsm3, 24, 31, 42], [etc]]





    def cluster(self, PCADataDF, PCADataNP):

        #first, we need to generate k clusters at random --> look at min and max of all dimensions to generate points:

        numDim = len(PCADataNP[1]) - 1
        minMaxList = minMax(PCADataDF)
        print("MinMax")
        print(minMaxList)
        #so for every kth cluster, we need to generate a point at random in numDim dimensions
        for k in range(self.k):
            self.centroids[k+1] = []
            for interval in minMaxList :
                randomPoint = random.uniform(interval[0], interval[1])
                self.centroids[k+1].append(randomPoint)

        #print (self.centroids)


        #begin the clustering algorithm

        #we go either until our centroids change by less than self.tolerance, or until we hit self.maxIters # of iterations
        for i in range(self.maxIters):
            print("\n\n\n\n----------------------------------NOW AT ITERATION STEP: %d ---------------------------\n\n\n\n\n" % (i))
            print("CURRENT CENTROIDS\n\n")
            print(self.centroids)
            print("\n\n\n CURRENT CLUSTERS\n\n")
            print(self.clusters)
            self.clusters = {}

            for k in range(self.k):
                self.clusters[k+1] = []

            #find the distance between each point and each centroid, then choose the nearest centroid
            for point in PCADataNP:
                distances = []
                for centroid in self.centroids:
                    distance = euclideanDistance(point[1:], self.centroids[centroid])
                    distances.append(distance)

                #here, i.e.  distances = [54.3, 524, 6213.151] for 3 clusters
                #we want the minimum distance and that argument:
                #then append that to the cluster that matches in self.clusters

                clusterToAssign = np.argmin(distances)+ 1
                #print(type(clusterToAssign))

                #print("assinging to cluster %d" % (clusterToAssign))
                self.clusters[clusterToAssign].append(point)

            #print(self.clusters[2])
            #print(self.clusters[2][1][1])
            #print(type(self.clusters[1]))
            #now we have a dictionary of clusters i.e. cluster1 : [GSM242, 333, 444, 555], [GSM424, 132, 234, 313] ... cluster 2:[GSM411, 222, 333, 444]...


            #first, we need to make a copy of the centroids so that we can compare how much they move after recalculation
            oldCentroids = dict(self.centroids)
            print("\n\n\n old centroid dictionary")

            print(oldCentroids)
            print("\n\n\n")
            #We need to recalculate centroids now --> taking the average
            sum = {}

            for centroid in self.centroids:

                sum[centroid] = [0] * numDim
                #print(sum[centroid])
                #averageOfCentroid = []
                numPoints = len(self.clusters[centroid])

                #if there are no points assigned to the centroid: assign a new random centroid
                if numPoints == 0:
                    dim = 0
                    for interval in minMaxList :
                        randomPoint = random.uniform(interval[0], interval[1])
                        print("\n\n\n\nRANDOM POINT")
                        print(randomPoint)
                        print(self.centroids[centroid])
                        self.centroids[centroid][dim] = randomPoint
                        dim += 1
                else:

                    print("Number of Points in the old centroid: %s" % (numPoints))
                    print("\n\n\nOld centroid points")


                    print(self.clusters[centroid])
                    for data in self.clusters[centroid]:

                        for index in range (1, numDim + 1):
                           sum[centroid][index - 1] += float(data[index])

                    averageOfCentroid = [x / numPoints for x in sum[centroid]]
                    print("\n\n\nSUM OF NEW CENTROID")
                    print(sum[centroid])
                    print("\n\n\nAVERAGE OF NEW CENTROID")
                    print(averageOfCentroid)
                    self.centroids[centroid] = averageOfCentroid

            print(oldCentroids)
            print(self.centroids)

            #now we test if the centroids have moved more than the self.tolerance (if we are converging)

            isDone = True

            for centroid in self.centroids:
                originalCentroid = oldCentroids[centroid]
                newCentroid = self.centroids[centroid]

                for dim in range(0, numDim):
                    if (abs(newCentroid[dim] - originalCentroid[dim]) > self.tolerance):
                        isDone = False
                        break

            if isDone:
                break

    def plotting(self, data):
        colors = 10 * ["r", "g", "c", "b", "k"]
        fig = plot.figure()
        ax = Axes3D(fig)

        for centroid in self.centroids:
            ax.scatter(self.centroids[centroid][0], self.centroids[centroid][1], self.centroids[centroid][2],  marker = "x")
        for data in self.clusters:
            color = colors[data]
            for features in self.clusters[data]:
                ax.scatter(features[1], features[2], features[3], color = color, s = 30)

                """  2D PLOTTING
        for centroid in self.centroids:
            plot.scatter(self.centroids[centroid][0], self.centroids[centroid][1], s = 130, marker = "x")

        for data in self.clusters:
            color = colors[data]
            for features in self.clusters[data]:
                plot.scatter(features[1], features[2], color = color, s = 30)
                """
        plot.show()

        #function to determine best number of K means --> via k means from 1 to kmax
        #elbow method using WWS, within-cluster-sum of squaured errors

def WSS(kmax, DF, NP):
    sse = []
    for k in range(1, kmax + 1):
        test = KMeans(k, 0.00001, 100)
        test.cluster(DF, NP)
        centroids = test.centroids
        clusters = test.clusters
        currentsse = 0
        for centroid in clusters:
            for point in clusters[centroid]:


                currentsse += euclideanDistance(centroids[centroid], point[1:])

        sse.append(currentsse)
    print("\n\n\nSSE:")
    print(sse)

    plot.plot(range(1, kmax + 1), sse, 'bx-')
    plot.show()
    return sse



def main():
    DF, NP = importData("PCA50.csv")
    WSS(7, DF, NP)
    #test = KMeans(5, 0.00001, 100)
    #test.cluster(DF, NP)
    #test.plotting(NP)

if __name__ == "__main__":
    main()
