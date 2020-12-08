import pandas as pd
from statistics import mean, stdev

def getStats(df, survivaldict):
	col = 'subtypes'
	list1 = df.loc[df[col] == 0, 'samples']
	list2 = df.loc[df[col] == 1, 'samples']
	list3 = df.loc[df[col] == 2, 'samples']
	list4 = df.loc[df[col] == 3, 'samples']
	list5 = df.loc[df[col] == 4, 'samples']
	vals1 = [float(survivaldict[i]) for i in list1 if (float(survivaldict[i]) > 0)]
	vals2 = [float(survivaldict[i]) for i in list2 if (float(survivaldict[i]) > 0)]
	vals3 = [float(survivaldict[i]) for i in list3 if (float(survivaldict[i]) > 0)]
	vals4 = [float(survivaldict[i]) for i in list4 if (float(survivaldict[i]) > 0)]
	vals5 = [float(survivaldict[i]) for i in list5 if (float(survivaldict[i]) > 0)]
	if vals1:
		mean1 = mean(vals1)
		std1 = stdev(vals1)
	else:
		mean1 = 'NA'
		std1 = ''
	
	if vals2:
		mean2 = mean(vals2)
		std2 = stdev(vals2)
	else:
		mean2 = 'NA'
		std2 = ''

	if vals3:
		mean3 = mean(vals3)
		std3 = stdev(vals3)
	else:
		mean3 = 'NA'
		std3 = ''
	if vals4:
		mean4 = mean(vals4)
		std4 = stdev(vals4)
	else:
		mean4 = 'NA'
		std4 = ''
	if vals5:
		mean5 = mean(vals5)
		std5 = stdev(vals5)
	else:
		mean5 = 'NA'
		std5 = ''
	print('Survival (months): ')
	print('Yellow: ', mean1, "+/-", std1)
	print('Blue: ', mean2, "+/-", std2)
	print('Green: ', mean3, "+/-", std3)
	print('Cyan: ', mean4, "+/-", std4)
	print('Red: ', mean5, "+/-", std5)

def getsubtypes():
	df = pd.read_csv('novel_results.csv')
	del df['Unnamed: 0']
	return df

def getmeta():
	f = open('GSE7696_series_matrix.txt')
	lines = f.readlines()
	i=0
	for line in lines:
		if "!Sample_geo_accession" in line:
			samples = line.split()
			samples.remove('!Sample_geo_accession')
			samples = [str(i).replace('"', '') for i in samples]
		if '!Sample_characteristics_ch1' in line:
			if 'survival time in months' in line:
				pre = line.split('\t')
				pre.remove('!Sample_characteristics_ch1')
				surv = [str(i).replace('survival time in months: ', '') for i in pre]
				surv = [str(i).replace('NA', '-100') for i in surv]
				surv = [str(i).replace('"', '') for i in surv]
				surv = [str(i).replace('\n', '') for i in surv]
	f.close()

	survivaldict = {samples[i]: surv[i] for i in range(len(samples))}
	return survivaldict


def main():
	df = getsubtypes()
	survivaldict = getmeta()
	getStats(df, survivaldict)

if __name__ == "__main__":
	main()