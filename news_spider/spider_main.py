import html_download, html_output, html_parse, url_manage


class SpiderMain(object):
    def __init__(self):
        # 将类赋给初始化变量
        self.urls = url_manage.UrlManage()
        self.download = html_download.HtmlDownload()
        self.parse = html_parse.HtmlParse()
        self.output = html_output.HtmlOutput()

    def craw(self, root_url, page_num):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("爬取到第", count, "个网页")
                html_contant = self.download.download(new_url)
                new_url, new_datas = self.parse.parse(root_url, html_contant, count)
                count = count + 1
                # print(new_url, " ", count)
                # for new_data in new_datas.items():
                #     print(new_data)
                self.urls.add_new_url(new_url)
                self.output.collection_data(new_datas)
                if count == page_num + 1:
                    break
            except:
                print("该url爬取失败")
        self.output.output_html()


if __name__ == "__main__":
    root_url = "http://www.jyb.cn/sy/zhxw/"
    page_num = 15
    obj_spider = SpiderMain()
    obj_spider.craw(root_url, page_num)
