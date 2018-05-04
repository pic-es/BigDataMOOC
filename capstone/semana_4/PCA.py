import numpy as np
from numpy.linalg import eigh
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, FloatType
from pyspark.mllib.linalg import Vectors, VectorUDT

# The following code has been copied from 
# https://stackoverflow.com/questions/33428589/pyspark-and-pca-how-can-i-extract-the-eigenvectors-of-this-pca-how-can-i-calcu


def estimateCovariance(df, features_col='features'):
    """Compute the covariance matrix for a given dataframe.

    Note:
        The multi-dimensional covariance array should be calculated using outer products.  Don't
        forget to normalize the data by first subtracting the mean.

    Args:
        df:  A Spark dataframe with a column named 'features', which (column) consists of DenseVectors.

    Returns:
        np.ndarray: A multi-dimensional array where the number of rows and columns both equal the
            length of the arrays in the input dataframe.
    """
    m = df.select(df[features_col]).map(lambda x: x[0]).mean()
    dfZeroMean = df.select(df[features_col]).map(lambda x:   x[0]).map(lambda x: x - m)  # subtract the mean

    return dfZeroMean.map(lambda x: np.outer(x,x)).sum()/df.count()

def pca(df, k=2, features_col='features'):
    """Computes the top `k` principal components, corresponding scores, and all eigenvalues.

    Note:
        All eigenvalues should be returned in sorted order (largest to smallest). `eigh` returns
        each eigenvectors as a column.  This function should also return eigenvectors as columns.

    Args:
        df: A Spark dataframe with a 'features' column, which (column) consists of DenseVectors.
        k (int): The number of principal components to return.

    Returns:
        tuple of (np.ndarray, RDD of np.ndarray, np.ndarray): A tuple of (eigenvectors, `RDD` of
        scores, eigenvalues).  Eigenvectors is a multi-dimensional array where the number of
        rows equals the length of the arrays in the input `RDD` and the number of columns equals
        `k`.  The `RDD` of scores has the same number of rows as `data` and consists of arrays
        of length `k`.  Eigenvalues is an array of length d (the number of features).
     """
    cov = estimateCovariance(df, features_col=features_col)
    col = cov.shape[1]
    eigVals, eigVecs = eigh(cov)
    inds = np.argsort(eigVals)
    eigVecs = eigVecs.T[inds[-1:-(col+1):-1]]  
    components = eigVecs[0:k]
    eigVals = eigVals[inds[-1:-(col+1):-1]]  # sort eigenvals
    #score = df.select(df[features_col]).map(lambda x: x[0]).map(lambda x: np.dot(x, components.T) )
    
    df = df.withColumn('score', project(components.T)(features_col))
    # Return the `k` principal components, `k` scores, and all eigenvalues

    #return components.T, score, eigVals
    return components.T, df, eigVals

def project(comp):
    return udf(lambda s: Vectors.dense(np.dot(s, comp)), VectorUDT())

def info_perc(eigVals, i):
    return 100*sum(eigVals[:i])/sum(eigVals)

# The previous code has been reformatted into this class. THAT ACTUALLY DOES NOT WORK!!!


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
        dfZeroMean = self.df_col.map(lambda x: x[0]).map(lambda x: x - self.mean)  # subtract the mean
        outer_prod_sum = dfZeroMean.map(lambda x: np.outer(x, x)).sum()
        self.cov = outer_prod_sum/self.or_df.count()

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
    