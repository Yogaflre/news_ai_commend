from operator import itemgetter


# 给指定用户推荐新闻
class CommendNews(object):
    def commend(self, user, trainset, usersset, simusers, recnuws):
        news = dict()
        watched_news = trainset[user]
        for sim_users, relation in sorted(usersset[user].items(), key=itemgetter(1), reverse=True)[0:simusers]:
            for new in trainset[sim_users]:
                if new in watched_news:
                    continue
                news.setdefault(new, 0)
                news[new] += relation
        return sorted(news.items(), key=itemgetter(1), reverse=True)[0:recnuws]
