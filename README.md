# GBMCluster

To use:
1. Given a dataset, download the series matrix file . txt.
2. In data.py, adjust the file location, skiprows, variance threshold, and out.csv file (contains
the PCA values). To visualize plot and heatmap uncomment end of file.
3. Run using the command: python data.py &rarr; this should output a csv file with the samples
and the PCA values
4. In kmeanscluster.py, change the location of the csv file in the main method, as well as
whether you want to run the WSS function to determine the optimal number of clusters
and/or the actual KMeans algorithm itself.
5. Run using the command: python kmeanscluster.py &rarr; this should generate an image of
the final clustering and elbow plot.
6. To validate the algorithm using the labeled dataset GSE72951 and to analyze prognosis
for the different subtypes, use the command: python validationrun.py &rarr; this should
generate 1) images of the true locations of the subtypes, the clusters produced by the
novel algorithm, and the clusters produced the sklearn algorithm, 2) statistics on the
accuracy of each algorithm, 3) average survival by subtype for each algorithm, and 4)
results for significance tests
