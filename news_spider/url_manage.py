class UrlManage(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    # 添加一个新的url
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:  # 若该url不再两个集合中，则添加到未爬取的set中
            self.new_urls.add(url)

    # 判断是否有新的url
    def has_new_url(self):
        return len(self.new_urls) != 0

    # 获取一个新的url
    def get_new_url(self):
        if self.has_new_url() is True:
            new_url = self.new_urls.pop()
            self.old_urls.add(new_url)
            return new_url
