import xlrd


# 加载数据的类
class LoadFile(object):
    # 加载一个文件，按照行循环输出
    def loadRating(self, file_path):
        file = open(file_path, 'r')
        for line in file:
            yield line.strip('\r\n')  # 返回执行结果并不中断程序
        file.close()

    def loadNews(self, commendset):
        if len(commendset) is 0:
            return "浏览记录不足"
        workbook = xlrd.open_workbook("../news_spider/news.xls")
        booksheet = workbook.sheet_by_name("Sheet1")
        # print("以下是为您推荐的新闻：")
        # print()
        num = 0
        commend_list = []
        for new, rate in commendset:
            num = num + 1
            # print(num, "、", booksheet.cell(int(new), 1).value, end=":")
            # print(booksheet.cell(int(new), 2).value)
            # print("感兴趣指数：", end=":")
            # print(rate)
            # print()
            news_name = booksheet.cell(int(new), 1).value
            news_url = booksheet.cell(int(new), 2).value
            commend_list.append([news_name, news_url, rate])
        return commend_list
