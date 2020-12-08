import validation
import sklearnrun
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def match(df, val):
	if val == 0:
		col = 'novel'
	else:
		col = 'sklearn'
	check1 = df.loc[df['samples'] == 'GSM1875232'][col].item()
	check2 = df.loc[df['samples'] == 'GSM1875196'][col].item()
	check3 = df.loc[df['samples'] == 'GSM1875269'][col].item()
	vals = []
	df[col] = df[col].replace([check1], '0!')
	vals.append(check1)
	df[col] = df[col].replace([check2], '2!')
	vals.append(check2)
	df[col] = df[col].replace([check3],'3!')
	vals.append(check3)
	if len(vals) == 3:
		for i in range(0,4):
			if i not in vals:
				df[col] = df[col].replace(i, '1!')

	df[col] = df[col].replace(['2!'], 2)
	df[col] = df[col].replace(['1!'], 1)
	df[col] = df[col].replace(['0!'], 0)
	df[col] = df[col].replace(['3!'], 3)
	check1 = df.loc[df['samples'] == 'GSM1875232'][col].item()
	check2 = df.loc[df['samples'] == 'GSM1875196'][col].item()
	check3 = df.loc[df['samples'] == 'GSM1875269'][col].item()
	return df

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
	ax.scatter(sub0['PC1'], sub0['PC2'], sub0['PC3'], color = 'r', s = 30)
	ax.scatter(sub1['PC1'], sub1['PC2'], sub1['PC3'], color = 'y', s = 30)
	ax.scatter(sub2['PC1'], sub2['PC2'], sub2['PC3'], color = 'b', s = 30)
	ax.scatter(sub3['PC1'], sub3['PC2'], sub3['PC3'], color = 'g', s = 30)
	plt.show()

	novel0 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['novel'] == 0].tolist())]
	novel1 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['novel'] == 1].tolist())]
	novel2 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['novel'] == 2].tolist())]
	novel3 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['novel'] == 3].tolist())]
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(novel0['PC1'], novel0['PC2'], novel0['PC3'], color = 'r', s = 30)
	ax.scatter(novel1['PC1'], novel1['PC2'], novel1['PC3'], color = 'y', s = 30)
	ax.scatter(novel2['PC1'], novel2['PC2'], novel2['PC3'], color = 'b', s = 30)
	ax.scatter(novel3['PC1'], novel3['PC2'], novel3['PC3'], color = 'g', s = 30)
	plt.show()

	sk0 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['sklearn'] == 0].tolist())]
	sk1 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['sklearn'] == 1].tolist())]
	sk2 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['sklearn'] == 2].tolist())]
	sk3 = coords.loc[coords['Sample'].isin(df['samples'].loc[df['sklearn'] == 3].tolist())]
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(sk0['PC1'], sk0['PC2'], sk0['PC3'], color = 'r', s = 30)
	ax.scatter(sk1['PC1'], sk1['PC2'], sk1['PC3'], color = 'y', s = 30)
	ax.scatter(sk2['PC1'], sk2['PC2'], sk2['PC3'], color = 'b', s = 30)
	ax.scatter(sk3['PC1'], sk3['PC2'], sk3['PC3'], color = 'g', s = 30)
	plt.show()

def analysis(df):
	match = 0
	mismatch = 0
	novelcorrect = sum(df['subtypes'] == df['novel'])
	novelincorrect = sum(df['subtypes'] != df['novel'])
	skcorrect = sum(df['subtypes'] == df['sklearn'])
	skincorrect = sum(df['subtypes'] != df['sklearn'])
	same = sum(df['novel'] == df['sklearn'])
	diff = sum(df['novel'] != df['sklearn'])
	print('NOVEL: ', '+:', novelcorrect, '-:', novelincorrect)
	print('SK: ', '+:', skcorrect, '-:', skincorrect)
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

def main():
	algoclusters, subtypedict = validation.main()
	skclusters = sklearnrun.main()
	df = pd.DataFrame(subtypedict.items(), columns = ['samples','subtypes'])
	df = clean(df)
	df = fromclusters(df, algoclusters, skclusters)
	for i in range(0, 2):
		df = match(df, i)
	coords = getcoords()
	graphs(df, coords)
	analysis(df)

if __name__ == "__main__":
	main()