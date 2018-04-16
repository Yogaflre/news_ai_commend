import load_file, create_dataset, commend_news


class CommendMain(object):
    def __init__(self):
        # 初始化类
        self.loadfile = load_file.LoadFile()
        self.createDataset = create_dataset.CreateDataset()
        self.commendNews = commend_news.CommendNews()

        self.trainset = {}  # 训练集
        self.testset = {}  # 测试集
        self.usersset = {}  # 用户关系集/相似矩阵
        self.commendset = {}  # 给用户推荐的新闻集合

        self.simusers = 4  # 推荐几个用户
        self.recnews = 5  # 推荐多少个新闻

    def training(self, rateing):
        trainset = self.trainset
        testset = self.testset
        usersset = self.usersset
        for line in self.loadfile.loadFile(rateing):
            trainset, testset = self.createDataset.generate_dataset(line, trainset, testset)
        print("训练集合：", trainset)
        # print("测试集合：",testset)
        usersset = self.createDataset.generate_users(trainset, usersset)
        # print("用户关系集合",usersset)
        usersset = self.createDataset.generate_relation(usersset, trainset)
        print("用户相似度矩阵", usersset)

    def commend(self, user):
        trainset = self.trainset
        usersset = self.usersset
        commendset = self.commendset
        simusers = self.simusers
        recnuws = self.recnews
        commendset = self.commendNews.commend(user, trainset, usersset, simusers, recnuws)
        print("给用户推荐的新闻编号和它的可能喜欢的程度：", commendset)


if __name__ == '__main__':
    rateing = "data/rateing.dat"
    news = "./news_spider/news.xls"
    user = "2"
    commendMain = CommendMain()
    commendMain.training(rateing)
    commendMain.commend(user)
