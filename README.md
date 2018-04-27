# news_ai_commend
教育新闻推荐

该项目主要分为两个板块：数据采集和推荐。

书籍采集采用python的urllib和BeautifulSoup库，推荐采用基于用户的协同过滤算法。


数据采集：

执行new_spider中的spider_main.py采集数据（默认采集150条新闻数据），采集后的新闻数据存放在news.xls中。


推荐：

执行new_recommend中的commend_main.py进行对于指定用户的推荐（默认用户id为2），采集后在控制台推荐的dict中键为推荐新闻的id，值为该新闻可能被喜欢的程度，值越大越符合用户的需求。通过更改commend_main.py主函数中的的user值，更改被推荐的用户id。

用户和新闻的关系数据来自于data中的rateing.dat。例如：“1::1n”，前者为用户的id，后者为书的id。
