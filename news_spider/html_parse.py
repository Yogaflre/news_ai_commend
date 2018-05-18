from bs4 import BeautifulSoup


class HtmlParse:
    def parse(self, page_url, html_contant, count):
        if page_url is None or html_contant is None:
            return None
        soup = BeautifulSoup(html_contant, 'html.parser', from_encoding='utf-8')
        new_url = self.get_new_url(page_url, count)
        new_datas = self.get_new_data(soup)
        return new_url, new_datas

    def get_new_url(self, page_url, count):
        new_url = page_url + 'index_' + str(count) + '.html'
        return new_url

    def get_new_data(self, soup):
        new_datas = {}
        a_s = soup.find_all("a", {"class": "title"})
        num = 0
        for a in a_s:
            new_datas[a['title']] = a['href']
            num = num + 1
            if num is 10:
                break
        return new_datas
