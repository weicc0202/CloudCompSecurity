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

class MySGD():
    def __init__(self, epoch, lr=1):
        self.epoch = epoch
        self.lr = lr

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def gradient(self, p, w):
        x, y = p.label, p.features
        return -self.sigmoid(-x * np.dot(w, y)) * x * y 
    
    def train(self, data):
        self.model = np.zeros(4) 
        for i in range(self.epoch):
            grad = data.map(lambda p: self.gradient(p, self.model)).reduce(lambda x, y: x + y)
            self.model -= self.lr * grad / data.count()
    
    def predict(self, features):
        y = self.sigmoid(np.dot(self.model, features))
        return round(y)



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
SGD = MySGD(
    epoch = 100
)
SGD.train(parsedData)
labelsAndPreds = parsedData.map(lambda point: (point.label, SGD.predict(point.features)))
trainErr = labelsAndPreds.filter(lambda p: p[0] != p[1]).count() / float(parsedData.count())
print("Training Error = " + str(trainErr))