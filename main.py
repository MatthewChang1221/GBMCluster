import validation
import sklearnrun
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
from statistics import mean, stdev

def main():
	valid = PCA()
	valid.datareduction(False)
	
	algoclusters, subtypedict, survivaldict = validation.main()
	skclusters = sklearnrun.main()
	df = pd.DataFrame(subtypedict.items(), columns = ['samples','subtypes'])
	df = clean(df)
	df = fromclusters(df, algoclusters, skclusters)
	for i in range(0, 2):
		df, loop = match(df, i, loop)
	coords = getcoords()
	graphs(df, coords)
	analysis(df)
	survivalanalysis(df, survivaldict)

if __name__ == "__main__":
	main()