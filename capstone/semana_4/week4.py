import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType

def ith_element(i):
    return udf(lambda v: float(v[i]), FloatType())

def describe_n(df, n_fields, input_col='features', output_str='feat_{0}'):
    for i in range(n_fields):
        df = df.withColumn(output_str.format(i), ith_element(i)(input_col))
    return df.select(*[output_str.format(i) for i in range(n_fields)]).toPandas().describe()


def confussion_matrix(pred_df, label_col='label', pred_col='prediction'):
    
    cm = pred_df.groupBy(label_col, pred_col).count().sort(label_col, pred_col)
    
    TN = cm.filter((cm.label == 0) & (cm.prediction == 0)).collect()[0][2]
    FP = cm.filter((cm.label == 0) & (cm.prediction == 1)).collect()[0][2]
    FN = cm.filter((cm.label == 1) & (cm.prediction == 0)).collect()[0][2]
    TP = cm.filter((cm.label == 1) & (cm.prediction == 1)).collect()[0][2]

    N = TN + FP + TP + FN

    Prev = (TP + FN) / N  
    Sens = TPR = Recall = TP / (TP + FN) 
    Esp  = TN / (TN + FP) #= (1 - FPR)
    Precision = PPV = TP / (TP + FP) 
    Acc = (TP + TN) / N


    print('Recall / Sensitivity / TPR = ', Sens)
    print('Specificity = 1 - FPR = ', Esp)
    print('Precision = ', Precision)
    print('Prevalence = ', Prev)
    print('Accuracy = ', Acc)
    
    return cm


def ROC_curve(pred_df, label_col='label', prob_col='probs', sample_size=0.1):
    
    df = pred_df.sample(False, sample_size).select(label_col, prob_col).toPandas()

    fpr, tpr, _ = roc_curve(df[label_col], df[prob_col])

    plt.plot(fpr, tpr)
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('Curva ROC')
    plt.show()