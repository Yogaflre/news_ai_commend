import xlwt


class HtmlOutput:
    def __init__(self):
        self.datas = []

    def collection_data(self, datas):
        if datas is None:
            return None
        self.datas.append(datas)

    def output_html(self):
        num = 1
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('Sheet1')
        booksheet.write(0, 0, "编号")
        booksheet.write(0, 1, "标题")
        booksheet.write(0, 2, "地址")
        for data in self.datas:
            for key in data:
                booksheet.write(num, 0, num)
                booksheet.write(num, 1, key)
                booksheet.write(num, 2, data[key])
                num = num + 1
        workbook.save('news.xls')
