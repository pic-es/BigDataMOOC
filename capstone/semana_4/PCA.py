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

def project(comp):
    return udf(lambda s: Vectors.dense(np.dot(s, comp)), VectorUDT())

class PCA():
    
    def fit(self, or_df, input_col='features'):
        # compute covariance
        cov = estimateCovariance(or_df, features_col=input_col)
        col = cov.shape[1]
        eigVals, eigVecs = eigh(cov)
        inds = np.argsort(eigVals)
        eigVecs = eigVecs.T[inds[-1:-(col + 1):-1]]  
        eigVals = eigVals[inds[-1:-(col + 1):-1]]  # sort eigenvals

        self.eigVecs = eigVecs
        self.eigVals = eigVals
    
    def transform(self, or_df, k, input_col='features', output_col='pca_features'):
        components = self.eigVecs[0:k].T
        df = or_df.withColumn(output_col, project(components)(input_col))
        return(df)
    
    def explained_variance(self, k):
        return sum(self.eigVals[0:k])/sum(self.eigVals)
    
    