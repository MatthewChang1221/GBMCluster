from data import PCA
import pandas as pd
import kmeanscluster
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def getmeta():
	f = open('validation_GSE72951_series_matrix.txt')
	lines = f.readlines()
	i=0
	for line in lines:
		if "!Sample_geo_accession" in line:
			samples = line.split()
			samples.remove('!Sample_geo_accession')
			samples = [str(i).replace('"', '') for i in samples]
		if '!Sample_characteristics_ch1' in line:
			if 'tcga subtype' in line:
				pre = line.split('\t')
				pre.remove('!Sample_characteristics_ch1')
				subtype = [str(i).replace('tcga subtype: ', '') for i in pre]
				subtype = [str(i).replace('"', '') for i in subtype]
				subtype = [str(i).replace('\n', '') for i in subtype]
			if 'survival (months)' in line:
				pre = line.split('\t')
				pre.remove('!Sample_characteristics_ch1')
				surv = [str(i).replace('survival (months): ', '') for i in pre]
				surv = [str(i).replace('sample type: FFPE', '-100') for i in surv]
				surv = [str(i).replace('"', '') for i in surv]
				surv = [str(i).replace('\n', '') for i in surv]
	f.close()

	subtypedict = {samples[i]: subtype[i] for i in range(len(samples))}
	survivaldict = {samples[i]: surv[i] for i in range(len(samples))}
	return subtypedict, survivaldict

# def plotreal(subtypedict):
# 	df = pd.read_csv('validationPCA90.csv')
# 	df.rename(columns = {'Unnamed: 0':'Sample'}, inplace = True)
# 	df['subtype'] = df['Sample'].map(subtypedict)

# 	classical = df.loc[df['subtype'] == 'Classical']
# 	mesenchymal = df.loc[df['subtype'] == 'Mesenchymal']
# 	neural = df.loc[df['subtype'] == 'Neural']
# 	proneural = df.loc[df['subtype'] == 'Proneural']
	
# 	fig = plt.figure()
# 	ax = Axes3D(fig)
# 	ax.scatter(classical['PC1'], classical['PC2'], classical['PC3'], color = 'y', s = 30)
# 	ax.scatter(mesenchymal['PC1'], mesenchymal['PC2'], mesenchymal['PC3'], color = 'b', s = 30)
# 	ax.scatter(neural['PC1'], neural['PC2'], neural['PC3'], color = 'r', s = 30)
# 	ax.scatter(proneural['PC1'], proneural['PC2'], proneural['PC3'], color = 'g', s = 30)
	
# 	# plt.show()
# 	plt.savefig('subtype_90.png')

def main():
	valid = PCA()
	valid.datareduction(True)
	# valid.PCA90.to_csv('validationPCA90.csv')
	# valid.PCA75.to_csv('validationPCA75.csv')
	# valid.PCA50.to_csv('validationPCA50.csv')
	subtypedict, survivaldict = getmeta()
	# plotreal(subtypedict)
	clusters = kmeanscluster.main(True)
	return clusters, subtypedict, survivaldict