from news_ai_commend.news_recommend import load_file, create_dataset, commend_evaluate
import matplotlib


class CommendMain(object):
    def __init__(self):
        # 初始化类
        self.loadfile = load_file.LoadFile()
        self.createDataset = create_dataset.CreateDataset()
        self.commendEvaluate = commend_evaluate.CommendEvaluate()

        self.trainset = {}  # 训练集
        self.testset = {}  # 测试集
        self.usersset = {}  # 用户关系集/相似矩阵
        self.commendset = []  # 给用户推荐的新闻集合

        self.simusers = 5  # 推荐几个用户
        self.recnews = 8  # 推荐多少个新闻

    def training(self, ratings):
        trainset = self.trainset
        testset = self.testset
        usersset = self.usersset
        for line in self.loadfile.loadRating(ratings):
            trainset, testset = self.createDataset.generate_dataset(line, trainset, testset)
        # trainset = self.createDataset.generate_originadd(rateing)
        print("训练集合：", trainset)

        # 生成用户关系集合
        usersset = self.createDataset.generate_users(trainset, usersset)
        print("用户关系集合", usersset)

        # 生成用户相似度矩阵
        usersset = self.createDataset.generate_relation(usersset, trainset)
        print("用户相似度矩阵", usersset)

    def commend(self, user):
        trainset = self.trainset
        usersset = self.usersset
        simusers = self.simusers
        recnuws = self.recnews
        commendset = self.createDataset.commend(user, trainset, usersset, simusers, recnuws)
        self.commendset = commendset
        print("给用户推荐的新闻编号和它的可能喜欢的程度：", commendset)
        commend_list = self.loadfile.loadNews(commendset)
        return commend_list

    def evaluate(self, user):
        commendset = self.commendset
        testset = self.testset
        print("推荐集合", commendset)
        print("测试集合", testset)
        sim_rate = self.commendEvaluate.commendEvaluate(user, commendset, testset,recnews,trainset)
        print(sim_rate)


if __name__ == '__main__':
    ratings = "data/ratings2.dat"
    user = "3"
    commendMain = CommendMain()
    commendMain.training(ratings)
    commend_dict = commendMain.commend(user)
    print(commend_dict)
    # commendMain.evaluate(user)
