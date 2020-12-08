from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def getdata():
    file = 'validation_GSE72951_series_matrix.txt'
    skip = 83
    df = pd.read_csv(file, delimiter='\t', skiprows=skip)
    df.drop(df.tail(1).index, inplace=True)
    df = df.set_index(['ID_REF'])
    df = df.transpose(copy=True)
    return df

def getsubtypes():
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
    f.close()

    subtypedict = {samples[i]: subtype[i] for i in range(len(samples))}
    return subtypedict

def runKmeans(df):
    data = df.to_numpy()
    kmeans = KMeans(n_clusters=4, random_state=0).fit(data)
    return kmeans.labels_.tolist()

def plotSKLearn(labels):
    df = pd.read_csv('validationPCA90.csv')
    df.rename(columns = {'Unnamed: 0':'Sample'}, inplace = True)
    type0idx = [i for i,x in enumerate(labels) if x == 0]
    type1idx = [i for i,x in enumerate(labels) if x == 1]
    type2idx = [i for i,x in enumerate(labels) if x == 2]
    type3idx = [i for i,x in enumerate(labels) if x == 3]
    
    type0 = df.iloc[type0idx]
    type1 = df.iloc[type1idx]
    type2 = df.iloc[type2idx]
    type3 = df.iloc[type3idx]

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(type0['PC1'], type0['PC2'], type0['PC3'], color = 'r', s = 30)
    ax.scatter(type1['PC1'], type1['PC2'], type1['PC3'], color = 'y', s = 30)
    ax.scatter(type2['PC1'], type2['PC2'], type2['PC3'], color = 'b', s = 30)
    ax.scatter(type3['PC1'], type3['PC2'], type3['PC3'], color = 'g', s = 30)
    # plt.show()

def compareresults(labels, subtype):
    subtypevals = []
    for i in subtype:
        if subtype[i] == 'Classical':
            subtypevals.append(1)
        if subtype[i] == 'Mesenchymal':
            subtypevals.append(2)
        if subtype[i] == 'Neural':
            subtypevals.append(0)
        if subtype[i] == 'Proneural':
            subtypevals.append(3)
    
    nc = 0
    nw = 0
    cc = 0
    cw = 0
    mc = 0
    mw = 0
    pc = 0
    pw = 0

    for i in range(len(subtypevals)): 
        if subtypevals[i] == 0:
            if subtypevals[i] == labels[i]:
               nc +=1
            else:
                nw +=1
        if subtypevals[i] == 1:
            if subtypevals[i] == labels[i]:
               cc +=1
            else:
                cw +=1
        if subtypevals[i] == 2:
            if subtypevals[i] == labels[i]:
               mc +=1
            else:
                mw +=1
        if subtypevals[i] == 3:
            if subtypevals[i] == labels[i]:
               pc +=1
            else:
                pw +=1
    print('neural', nc, nw)
    print('clinical', cc, cw)
    print('Mesenchymal', mc, mw)
    print('Proneural', pc, pw)

def main():
    df = getdata()
    labels = runKmeans(df)
    subtypes = getsubtypes()
    # plotSKLearn(labels)
    return labels

if __name__ == "__main__":
    main()