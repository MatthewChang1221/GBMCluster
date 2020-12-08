import validation
import sklearnrun
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
from statistics import mean, stdev

def fromclusters(df, algoclusters, skclusters):
	cluster1 = [i[0] for i in algoclusters[1]]
	cluster2 = [i[0] for i in algoclusters[2]]
	cluster3 = [i[0] for i in algoclusters[3]]
	cluster4 = [i[0] for i in algoclusters[4]]

	clusters = {i : 0 for i in cluster1}
	for i in cluster2:
		clusters[i] = 1
	for i in cluster3:
		clusters[i] = 2
	for i in cluster4:
		clusters[i] = 3

	df['novel'] = df['samples'].map(clusters)
	df['sklearn'] = skclusters
	return df	

def clean(df):
	#classical = 0, mesenchymal = 1, neural = 2, proneural = 3
	df['subtypes'].replace('Classical',0,inplace=True)
	df['subtypes'].replace('Mesenchymal',1,inplace=True)
	df['subtypes'].replace('Neural',2,inplace=True)
	df['subtypes'].replace('Proneural',3,inplace=True)
	return df

def match(df, val, loop):
	if val == 0:
		col = 'novel'
	else:
		col = 'sklearn'
	check1 = df.loc[df['samples'] == 'GSM1875232'][col].item()
	check1b = df.loc[df['samples'] == 'GSM1875197'][col].item()
	check1c = df.loc[df['samples'] == 'GSM1875232'][col].item()
	lst = [check1, check1b, check1c]
	check2 = df.loc[df['samples'] == 'GSM1875196'][col].item()
	check3 = df.loc[df['samples'] == 'GSM1875269'][col].item()
	vals = []
	df[col] = df[col].replace([check2], '2!')
	vals.append(check2)
	df[col] = df[col].replace([check3],'3!')
	vals.append(check3)
	mode = stats.mode(lst)[0]
	df[col] = df[col].replace([mode], '0!')
	vals.append(mode)
	if len(vals) == 3:
		for i in range(0,4):
			if i not in vals:
				df[col] = df[col].replace(i, '1!')

	df[col] = df[col].replace(['2!'], 2)
	df[col] = df[col].replace(['1!'], 1)
	df[col] = df[col].replace(['0!'], 0)
	df[col] = df[col].replace(['3!'], 3)
	if df['novel'].nunique() == 4:
		loop = False
	return df, loop

def getcoords():
	coords = pd.read_csv('validationPCA90.csv')
	coords.rename(columns = {'Unnamed: 0':'Sample'}, inplace = True)
	return coords

def graphs(df, coords):
	#classical = 0, mesenchymal = 1, neural = 2, proneural = 3
	sub0 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['subtypes'] == 0].tolist())]
	sub1 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['subtypes'] == 1].tolist())]
	sub2 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['subtypes'] == 2].tolist())]
	sub3 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['subtypes'] == 3].tolist())]
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(sub0['PC1'], sub0['PC2'], sub0['PC3'], color = 'r', s = 30, label='classical')
	ax.scatter(sub1['PC1'], sub1['PC2'], sub1['PC3'], color = 'y', s = 30, label='mesenchymal')
	ax.scatter(sub2['PC1'], sub2['PC2'], sub2['PC3'], color = 'b', s = 30, label='neural')
	ax.scatter(sub3['PC1'], sub3['PC2'], sub3['PC3'], color = 'g', s = 30, label='proneural')
	plt.legend(loc="upper left")
	ax.set_xlabel('PCA1', rotation=-30)
	ax.set_ylabel('PCA2', rotation=60)
	ax.set_zlabel('PCA3', rotation=90)
	fig.suptitle('Known Subtypes', fontsize=12)
	plt.savefig('validation_subtype.png')

	novel0 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['novel'] == 0].tolist())]
	novel1 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['novel'] == 1].tolist())]
	novel2 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['novel'] == 2].tolist())]
	novel3 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['novel'] == 3].tolist())]
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(novel0['PC1'], novel0['PC2'], novel0['PC3'], color = 'r', s = 30, label='classical')
	ax.scatter(novel1['PC1'], novel1['PC2'], novel1['PC3'], color = 'y', s = 30, label='mesenchymal')
	ax.scatter(novel2['PC1'], novel2['PC2'], novel2['PC3'], color = 'b', s = 30, label='neural')
	ax.scatter(novel3['PC1'], novel3['PC2'], novel3['PC3'], color = 'g', s = 30, label='proneural')
	fig.suptitle('Predicted Subtypes (Novel)', fontsize=12)
	ax.set_xlabel('PCA1', rotation=-30)
	ax.set_ylabel('PCA2', rotation=60)
	ax.set_zlabel('PCA3', rotation=90)
	plt.legend(loc="upper left")
	plt.savefig('validation_novel.png')

	sk0 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['sklearn'] == 0].tolist())]
	sk1 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['sklearn'] == 1].tolist())]
	sk2 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['sklearn'] == 2].tolist())]
	sk3 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['sklearn'] == 3].tolist())]
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(sk0['PC1'], sk0['PC2'], sk0['PC3'], color = 'r', s = 30, label='classical')
	ax.scatter(sk1['PC1'], sk1['PC2'], sk1['PC3'], color = 'y', s = 30, label='mesenchymal')
	ax.scatter(sk2['PC1'], sk2['PC2'], sk2['PC3'], color = 'b', s = 30, label='neural')
	ax.scatter(sk3['PC1'], sk3['PC2'], sk3['PC3'], color = 'g', s = 30, label='proneural')
	fig.suptitle('Predicted Subtypes (SKLearn)', fontsize=12)
	ax.set_xlabel('PCA1', rotation=-30)
	ax.set_ylabel('PCA2', rotation=60)
	ax.set_zlabel('PCA3', rotation=90)
	plt.legend(loc="upper left")
	plt.savefig('validation_sklearn.png')

def analysis(df):
	match = 0
	mismatch = 0
	novelcorrect = sum(df['subtypes'] == df['novel'])
	novelincorrect = sum(df['subtypes'] != df['novel'])
	skcorrect = sum(df['subtypes'] == df['sklearn'])
	skincorrect = sum(df['subtypes'] != df['sklearn'])
	same = sum(df['novel'] == df['sklearn'])
	diff = sum(df['novel'] != df['sklearn'])
	print('NOVEL: ', 'Correct:', novelcorrect, 'Incorrect:', novelincorrect, '% Correct: ', (novelincorrect/(novelcorrect+novelincorrect))*100, '%')
	print('SK: ', 'Correct:', skcorrect, 'Incorrect:', skincorrect, '% Correct: ', (skcorrect/(skcorrect+skincorrect))*100, '%')
	print('Compare: ', 'same: ', same, 'diff: ', diff)
	df = df.replace({0: 'classical'})
	df = df.replace({1: 'mesenchymal'})
	df = df.replace({2: 'neural'})
	df = df.replace({3: 'proneural'})
	for i in range(0,2):
		if i == 0: 
			col = 'novel'
		else:
			col = 'sklearn'
		rates = {'classical': {'match':0, 'overpredicted':0, 'missed':0},
					'mesenchymal': {'match':0, 'overpredicted':0, 'missed':0},
					'neural': {'match':0, 'overpredicted':0, 'missed':0},
					'proneural': {'match':0, 'overpredicted':0, 'missed':0}}
		for i in range(0, len(df)):
			if df['subtypes'][i] == df[col][i]:
				rates[df[col][i]]['match'] += 1
			else:
				rates[df[col][i]]['overpredicted'] += 1
				rates[df['subtypes'][i]]['missed'] += 1
		print(col, ": ", rates)

def getSamples(df, val, survivaldict):
	if val == 0:
		col = 'subtypes'
	elif val == 1:
		col = 'novel'
	else:
		col = 'sklearn'
	clist = df.loc[df[col] == 0, 'samples']
	mlist = df.loc[df[col] == 1, 'samples']
	nlist = df.loc[df[col] == 2, 'samples']
	plist = df.loc[df[col] == 3, 'samples']
	cvals = [float(survivaldict[i]) for i in clist if (float(survivaldict[i]) > 0)]
	mvals = [float(survivaldict[i]) for i in mlist if (float(survivaldict[i]) > 0)]
	nvals = [float(survivaldict[i]) for i in nlist if (float(survivaldict[i]) > 0)]
	pvals = [float(survivaldict[i]) for i in plist if (float(survivaldict[i]) > 0)]
	cmean = mean(cvals)
	mmean = mean(mvals)
	nmean = mean(nvals)
	pmean = mean(pvals)
	cstd = stdev(cvals)
	mstd = stdev(mvals)
	nstd = stdev(nvals)
	pstd = stdev(pvals)

	return cmean, mmean, nmean, pmean, cstd, mstd, nstd, pstd
	

def survivalanalysis(df, survivaldict):
	cmean, mmean, nmean, pmean, cstd, mstd, nstd, pstd = getSamples(df, 0, survivaldict)
	novelcmean, novelmmean, novelnmean, novelpmean, novelcstd, novelmstd, novelnstd, novelpstd = getSamples(df, 1, survivaldict)
	skcmean, skmmean, sknmean, skpmean, skcstd, skmstd, sknstd, skpstd = getSamples(df, 2, survivaldict)
	print('Given survival (months): ', 'C: ', cmean, 'M: ', mmean, 'N: ', nmean, 'P: ', pmean)
	print('Novel survival (months): ', 'C: ', novelcmean, 'M: ', novelmmean, 'N: ', novelnmean, 'P: ', novelpmean)
	print('Sklearn survival (months): ', 'C: ', skcmean, 'M: ', skmmean, 'N: ', sknmean, 'P: ', skpmean)
	print('Differences (novel): ', 'C: ', cmean-novelcmean, 'M: ', mmean-novelmmean, 'N: ', nmean-novelnmean, 'P: ', pmean-novelpmean)
	print('Differences (sklearn): ', 'C: ', cmean-skcmean, 'M: ', mmean-skmmean, 'N: ', nmean-sknmean, 'P: ', pmean-skpmean)


def main():
	loop = True
	while(loop):
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