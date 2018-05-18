from operator import itemgetter


# 给指定用户推荐新闻
class CommendNews(object):
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
