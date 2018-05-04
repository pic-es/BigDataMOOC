from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType

def ith_element(i):
    return udf(lambda v: float(v[i]), FloatType())

def describe_n(df, n_fields, input_col='features', output_str='feat_{0}'):
    for i in range(n_fields):
        df = df.withColumn(output_str.format(i), ith_element(i)(input_col))
    return df.select(*[output_str.format(i) for i in range(n_fields)]).toPandas().describe()