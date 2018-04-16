from urllib import request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context  # python3中需要取消证书验证


class HtmlDownload:
    def download(self, url):
        if url is None:
            return None
        response = request.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()
