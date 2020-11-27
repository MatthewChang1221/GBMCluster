import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class PCA:
    def __init__(self):
        self.PCA50 = None
        self.PCA75 = None
        self.PCA90 = None

    def datareduction(self):
        df = pd.read_csv('GSE7696_series_matrix.txt', delimiter='\t', skiprows=93)
        df.drop(df.tail(1).index, inplace=True)
        df = df.set_index(['ID_REF'])
        df = df.transpose(copy=True)
        print(df)
        '''
        print("\n\nNumber of features in the dataset :\n", '#' * 40)
        print("\nFeatures Set : \n", '-' * 20, len(df.columns))
        
        # print("\n\nFeatures in the dataset :\n", '#' * 40)
        # print("\nFeatures Set : \n", list(df.columns))
        
        print("\n\nDatatypes of features and labels in the dataset :\n", '#' * 40)
        print("\nFeatures Set : \n", '-' * 20, "\n", df.dtypes)
        
        print("\n\nNumber of observations in the dataset :\n", '#' * 40)
        print("\nFeatures Set : \n", '-' * 20, len(df))
        
        print("\n\nEmpty cells or Nans in the dataset :\n", '#' * 40)
        print("\nFeatures Set : \n", '-' * 20, df.isnull().values.any())
        
        print("\n\nNumber of empty cells or Nans in the dataset :\n", '#' * 40)
        print("\nFeatures Set : \n", '-' * 20, "\n", df.isnull().sum())
        
        print("\n\nRange of data :\n", '#' * 40)
        # print("\nFeatures Set : \n", '-' * 20, "\n", df.apply(lambda x: round(x.max()-x.min())).to_string())
        '''

        # Standardization of Data: This can be removed if not needed since data is relatively of the same scale and unit
        from sklearn.preprocessing import StandardScaler

        x = df.values
        #x = StandardScaler().fit_transform(x)

        # Feature Filtering : Removing features with less than x variance
        from sklearn.feature_selection import VarianceThreshold

        selector_50 = VarianceThreshold(0.05987)  # Threshold that keeps 50% of genes = 0.05987, 75% of genes = 0.1841,
                                                  # 90% = 0.4315
        selector_75 = VarianceThreshold(0.1841)
        selector_90 = VarianceThreshold(0.4315)
        x_75 = selector_75.fit_transform(x)
        x_50 = selector_50.fit_transform(x)
        x_90 = selector_90.fit_transform(x)

        df_50 = df[df.columns[selector_50.get_support(indices=True)]]
        df_75 = df[df.columns[selector_75.get_support(indices=True)]]
        df_90 = df[df.columns[selector_90.get_support(indices=True)]]

        #print(np.mean(x, axis=0).min())


        from sklearn.decomposition import PCA

        pca = PCA(n_components=3)
        pca_GCM_50 = pca.fit_transform(x_50)
        pca_GCM_75 = pca.fit_transform(x_75)
        pca_GCM_90 = pca.fit_transform(x_90)

        self.PCA50 = pd.DataFrame(pca_GCM_50, columns=['PC1', 'PC2', 'PC3'],index=df_50.index)
        self.PCA75 = pd.DataFrame(pca_GCM_75, columns=['PC1', 'PC2', 'PC3'],index=df_75.index)
        self.PCA90 = pd.DataFrame(pca_GCM_90, columns=['PC1', 'PC2', 'PC3'],index=df_90.index)

        #print(pca_GCM_df_90)

        print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_)) # this for the 90%

        # To plot just uncomment and change the value of the df to the variation level you want

        '''
        plt.figure(figsize=(10, 10))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=14)
        plt.xlabel('Principal Component 1', fontsize=20)
        plt.ylabel('Principal Component 2', fontsize=20)
        plt.title('PCA of GSE7696 Genes for GBM', fontsize=20)
        plt.scatter(pca_GCM_df['PC1'], pca_GCM_df['PC2'])
        plt.show()
        
        pca2 = PCA().fit(x)
        plt.scatter([x for x in range(len(pca2.explained_variance_ratio_))], pca2.explained_variance_ratio_)
        plt.xlabel('number of components')
        plt.ylabel('explained variance')
        plt.show()
        
        correlation = df.corr()
        ax = sns.heatmap(correlation,
                         vmin=-1,
                         vmax=1,
                         center=0,
                         cmap=sns.diverging_palette(20, 220, n=200),
                         square=True)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right');
        plt.title('Heatmap of 22 Most Varied Probe Sets based on Correlations', fontsize=20)
        plt.show()
        '''

