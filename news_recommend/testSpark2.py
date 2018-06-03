from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row, SparkSession
from news_ai_commend.news_recommend import load_file


class testSparkMain2(object):
    def __init__(self):
        self.trainset = {}  # 训练集
        self.testset = {}  # 测试集

        self.simusers = 5  # 推荐几个用户
        self.recnews = 8  # 推荐多少个新闻

    def test(self, user):
        # conf = SparkConf().setMaster("local")
        # sc = SparkContext(conf=conf)
        # text_file = sc.textFile(
        #     "/Users/yogafire/Documents/Projects-Pycharm/news_ai_commend/news_recommend/data/ratings2.dat")
        # origin_rdd = text_file.map(lambda line: line.split("::"))

        spark = SparkSession.builder.appName("RDD_and_DataFrame").config("spark.some.config.option",
                                                                         "some-value").getOrCreate()
        # 加载外部数据集
        text_file = spark.read.text(
            "/Users/yogafire/Documents/Projects-Pycharm/news_ai_commend/news_recommend/data/ratings2.dat").rdd
        origin_rdd = text_file.map(lambda line: line.value.split("::"))
        ratings_rdd = origin_rdd.map(lambda p: Row(userId=int(p[0]), newsId=int(p[1]), rating=int(p[2])))
        # rateings_DF = spark.createDataFrame(rateings_rdd)
        ratings_DF = ratings_rdd.toDF()
        traing_DF, test_DF = ratings_DF.randomSplit([0.7, 0.3])

        als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="newsId", ratingCol="rating")
        model = als.fit(traing_DF)

        # 推荐
        user_subset = ratings_DF.where(ratings_DF.userId == user)
        print("用户浏览集合：", user_subset.toJSON().collect())

        traing_subset = traing_DF.where(traing_DF.userId == user)
        print("用户训练集合：", traing_subset.toJSON().collect())

        test_subset = test_DF.where(test_DF.userId == user)
        print("用户测试集合:", test_subset.toJSON().collect())

        recommend_DF = model.recommendForUserSubset(user_subset, 150)
        print("用户推荐集合：", recommend_DF.toJSON().collect())

        recommend_IT = recommend_DF.toLocalIterator()

        news = {}
        watched_news = []
        for news_watched, rating_watched, userId in traing_subset.toLocalIterator():
            watched_news.append(news_watched)

        for userId, recommendations in recommend_IT:
            for news_recommend, rating_recommend in recommendations:
                if news_recommend in watched_news:
                    continue
                news.setdefault(news_recommend, rating_recommend)
                if len(news) == 8:
                    break
        print("新闻&评分预测：", news)

        commend_list = load_file.LoadFile().loadNews(news.items())
        print("推荐的新闻：", commend_list)

        # 测试
        predictions = model.transform(test_DF)
        evaluator = RegressionEvaluator().setMetricName("rmse").setLabelCol("rating").setPredictionCol("prediction")
        rmse = evaluator.evaluate(predictions)
        print(rmse)

        return commend_list, rmse


if __name__ == '__main__':
    testSparkMain2 = testSparkMain2()
    testSparkMain2.test("4")
