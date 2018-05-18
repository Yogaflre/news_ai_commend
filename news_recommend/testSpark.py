from pyspark import SparkConf, SparkContext
import load_file, create_dataset, commend_news, math
from operator import itemgetter


class testSparkMain(object):
    def __init__(self):
        self.loadfile = load_file.LoadFile()
        self.createDataset = create_dataset.CreateDataset()

        self.trainset = {}  # 训练集
        self.testset = {}  # 测试集

        self.simusers = 5  # 推荐几个用户
        self.recnews = 8  # 推荐多少个新闻

    def new(self, train_rdd, key):
        for rdd in train_rdd.collect():
            if rdd[0] == key:
                return len(rdd[1])

    def to_list(self, a):
        return [a]

    def append(self, a, b):
        a.append(b)
        return a

    def extend(self, a, b):
        a.extend(b)
        return a

    def getValuesByKey(self, train_rdd, user):
        for key, value in train_rdd.collect():
            if key == user:
                return value

    def test(self):
        trainset = {}
        testset = {}
        usersset = {}
        news = {}
        # 初始化Spark
        conf = SparkConf().setMaster("local").setAppName("news_recommend")
        sc = SparkContext(conf=conf)
        # 加载外部数据集
        text_file = sc.textFile("data/rateing.dat")
        origin_rdd = text_file.map(lambda line: line.split("::"))
        print("origin_rdd", origin_rdd.collect())
        # 生成用户/新闻关系表
        train_rdd = origin_rdd.combineByKey(self.to_list, self.append, self.extend)
        print("train_rdd", train_rdd.collect())

        # print(train_map.lookup('1'))

        # 生成用户/新闻关系表
        # for string in text_file.collect():
        #     user, new = string.split("::")
        #     trainset.setdefault(user, set())
        #     trainset[user].add(new)
        # train_map = sc.parallelize(trainset).map(lambda x: (x, trainset.get(x)))
        # print(train_map.collect())

        # 生成用户关系表
        for map1 in train_rdd.collect():
            for map2 in train_rdd.collect():
                if map1[0] == map2[0]:
                    continue
                # num = len(map1[1] & map2[1])
                num = len(set(map1[1]) & set(map2[1]))
                if num is not 0:
                    usersset.setdefault(map1[0], {})
                    usersset[map1[0]].setdefault(map2[0], num)
        user_rdd = sc.parallelize(usersset).map(lambda x: (x, usersset.get(x)))
        print("user_rdd", user_rdd.collect())

        # 生成用户相似度表
        for map3 in user_rdd.collect():
            for user, count in map3[1].items():
                usersset[map3[0]][user] = count / math.sqrt(
                    len(self.getValuesByKey(train_rdd, map3[0])) * len(self.getValuesByKey(train_rdd, user)))
        user_rdd = sc.parallelize(usersset).map(lambda x: (x, usersset.get(x)))
        print("user_rdd", user_rdd.collect())

        watched_news = self.getValuesByKey(train_rdd, "1")
        print("watched_news", watched_news)

        print(usersset["1"].items())
        print(self.getValuesByKey(user_rdd, "1"))

        # 给用户推荐新闻
        for sim_users, rate in sorted(list(self.getValuesByKey(user_rdd, "1")), key=itemgetter(1), reverse=True)[
                               0:self.simusers]:
            for new in self.getValuesByKey(train_rdd, sim_users):
                if new in watched_news:
                    continue
                news.setdefault(new, 0)
                news[new] += rate
        commend_rdd = sorted(news.items(), key=itemgetter(1), reverse=True)[0:self.recnews]
        print(commend_rdd)


if __name__ == '__main__':
    testSparkMain = testSparkMain()
    testSparkMain.test()
