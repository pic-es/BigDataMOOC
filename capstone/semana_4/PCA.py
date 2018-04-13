import numpy as np
from numpy.linalg import eigh

class PCA():
    
    def fit(self, or_df, input_col='features'):
        
        self.or_df = or_df
        self.input_col = input_col
        self.df_col = self.or_df.select(input_col)
        self.count = self.df_col.count()
        self.compute_mean()
        self.compute_cov()
        self.compute_pca()
    
    def compute_mean(self):
        self.mean = self.df_col.map(lambda x: x[0]).mean() 
    
    def compute_cov(self):
        """Compute the covariance matrix of a dataframe input column.
        """
        self.dfZeroMean = self.df_col.map(lambda x: x[0]).map(lambda x: x - self.mean)  # subtract the mean
        self.outer_prod = self.dfZeroMean.map(lambda x: np.outer(x, x))
        self.outer_prod_sum = self.outer_prod.sum()
        self.cov = self.outer_prod_sum/self.count

    def compute_pca(self):
        """Computes the principal components, corresponding scores, and all eigenvalues.
         """
        col = self.cov.shape[1]
        eigVals, eigVecs = eigh(self.cov)
        inds = np.argsort(eigVals)
        eigVecs = eigVecs.T[inds[-1:-(col + 1):-1]]  
        eigVals = eigVals[inds[-1:-(col + 1):-1]]  # sort eigenvals
        score = self.df_col.map(lambda x: x[0]).map(lambda x: np.dot(x, eigVecs.T))

        self.score = score
        self.eigVecs = eigVecs.T
        self.eigVals = eigVals
    
    def explained_variance(self, k):
        return sum(self.eigVals[0:k])/sum(self.eigVals)
    