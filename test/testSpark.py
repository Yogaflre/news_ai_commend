from pyspark import SparkConf, SparkContext

# 初始化Spark
conf = SparkConf().setMaster("local").setAppName("test")
sc = SparkContext(conf=conf)


# add = [1, 2, 3, 4, 5]
# data = sc.parallelize(add, 5)
# print(data.foreach())

# 加载外部数据集
text_file = sc.textFile("test.txt")
print(text_file.count())
