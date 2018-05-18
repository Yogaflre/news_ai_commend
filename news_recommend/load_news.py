import xlrd


class LoadNews(object):
    def loadNews(self, commendset):
        if len(commendset) is 0:
            return "浏览记录不足"
        workbook = xlrd.open_workbook("../news_spider/news.xls")
        booksheet = workbook.sheet_by_name("Sheet1")
        print("以下是为您推荐的新闻：")
        print()
        num = 0
        for new, rate in commendset:
            num = num + 1
            print(num, "、", booksheet.cell(int(new), 1).value, end=":")
            print(booksheet.cell(int(new), 2).value)
            print("感兴趣指数：", end=":")
            print(rate)
            print()
