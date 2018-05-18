import random
import math


# 处理数据的类
class CreateDataset(object):
    # 生成两个数据集：训练集和测试集合
    def generate_dataset(self, line, trainset, testset, pivot=0.5):
        user, new = line.split('::')
        # if (random.random() < pivot):
        if (True):
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