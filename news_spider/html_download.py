from urllib import request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context  # python3中需要取消证书验证

header_dict = {  # 创建一个headers的集合（伪装成浏览器）
    'User-Agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
}


class HtmlDownload:
    def download(self, url):
        if url is None:
            return None
        req = request.Request(url=url, headers=header_dict)
        response = request.urlopen(req)
        if response.getcode() != 200:
            return None
        return response.read()
