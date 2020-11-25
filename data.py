import pandas as pd

df = pd.read_csv('GSE7696_series_matrix.txt', delimiter='\t', skiprows=93)
df.drop(df.tail(1).index, inplace=True)
df = df.set_index(['ID_REF'])
df = df.transpose(copy=True)
print(df)

print("\n\nNumber of features in the dataset :\n", '#' * 40)
print("\nFeatures Set : \n", '-' * 20, len(df.columns))

#print("\n\nFeatures in the dataset :\n", '#' * 40)
#print("\nFeatures Set : \n", list(df.columns))

print("\n\nDatatypes of features and labels in the dataset :\n", '#' * 40)
print("\nFeatures Set : \n", '-' * 20, "\n", df.dtypes)

print("\n\nNumber of observations in the dataset :\n", '#' * 40)
print("\nFeatures Set : \n", '-' * 20, len(df))

print("\n\nEmpty cells or Nans in the dataset :\n", '#' * 40)
print("\nFeatures Set : \n", '-' * 20, df.isnull().values.any())

print("\n\nNumber of empty cells or Nans in the dataset :\n", '#' * 40)
print("\nFeatures Set : \n", '-' * 20, "\n", df.isnull().sum())

print("\n\nRange of data :\n", '#' * 40)
print("\nFeatures Set : \n", '-' * 20, "\n", df.apply(lambda x: round(x.max()-x.min())).to_string())

