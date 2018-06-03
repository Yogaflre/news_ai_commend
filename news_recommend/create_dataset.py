import math
import random
from operator import itemgetter


# 处理数据的类
class CreateDataset(object):
    # 生成两个数据集：训练集和测试集合
    def generate_dataset(self, line, trainset, testset, pivot=0.7):
        user, new, rating = line.split('::')
        if (random.random() < pivot):
            # if (True):
            trainset.setdefault(user, set())
            trainset[user].add(new)
            # trainset[user][new] = int(rating)
        else:
            testset.setdefault(user, set())
            testset[user].add(new)
        return trainset, testset

    # 生成用户关系集合
    def generate_users(self, trainset, usersset):
        for user1, news1 in trainset.items():
            for user2, news2 in trainset.items():
                if user1 == user2:
                    continue
                num = len(news1 & news2)
                if num is not 0:
                    usersset.setdefault(user1, {})
                    usersset[user1].setdefault(user2, num)
        return usersset

    # 生成用户相似度矩阵(余弦相似度)
    def generate_relation(self, usersset, trainset):
        for user1, relation in usersset.items():
            for user2, count in relation.items():
                usersset[user1][user2] = count / math.sqrt(len(trainset[user1]) * len(trainset[user2]))
        return usersset

    # 生成指定用户的推荐列表
    def commend(self, user, trainset, usersset, simusers, recnews):
        news = {}
        # 获取该用户已经看过的新闻
        watched_news = trainset[user]
        for sim_users, rate in sorted(usersset[user].items(), key=itemgetter(1), reverse=True)[0:simusers]:
            for new in trainset[sim_users]:
                if new in watched_news:
                    continue
                news.setdefault(new, 0)
                news[new] += rate
        return sorted(news.items(), key=itemgetter(1), reverse=True)[0:recnews]
