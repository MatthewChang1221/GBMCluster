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