from pyspark.mllib.classification import LogisticRegressionWithSGD
import numpy as np
from pyspark import SparkConf, SparkContext
from pyspark.mllib.regression import LabeledPoint


def getSparkContext():
    """
    Gets the Spark Context
    """
    conf = (SparkConf()
         .setMaster("local") # run on local
         .setAppName("Logistic Regression") # Name of App
         .set("spark.executor.memory", "1g")) # Set 1 gig of memory
    sc = SparkContext(conf = conf) 
    return sc

sc = getSparkContext()

# Load and parse the data
data = sc.textFile("/data.txt")

def mapper(line):
    """
    Mapper that converts an input line to a feature vector
    """    
    values = [float(x) for x in line.split(',')]
    return LabeledPoint(values[-1], values[:-1])

parsedData = data.map(mapper)

model = LogisticRegressionWithSGD.train(parsedData, iterations=100)

labelsAndPreds = parsedData.map(lambda point: (point.label, model.predict(point.features)))

trainErr = labelsAndPreds.filter(lambda p: p[0] != p[1]).count() / float(parsedData.count())
print("Training Error = " + str(trainErr))


