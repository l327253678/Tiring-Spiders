# -*- coding: utf-8 -*- 
# @Author : Leo


import re
import requests
from lxml import etree
from io import BytesIO
from fontTools.ttLib import TTFont

"""
起点中文网-字体反爬
"""


class QidianSpider:
    """起点中文网爬虫"""

    session = requests.session()

    # 字体文件路径
    font_path = None
    # 字体缓存
    font_cache = None

    def __init__(self):
        # 首页地址
        self.home_url = 'https://www.qidian.com/all?&page=1'
        # 请求头headers
        self.headers = {
            'Host': 'www.qidian.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

        self.session.headers.update(self.headers)

    def crawl(self):
        """采集首页"""
        resp = self.session.get(url=self.home_url)
        if resp.status_code == 200:
            html = etree.HTML(resp.text)
            books_tags = html.xpath('//div[@class="all-book-list"]//li[@data-rid]')
            for each_book in books_tags:
                book_info = dict()
                book_info['id'] = each_book.xpath('.//h4/a[@href and @data-bid]/@data-bid')[0]
                book_info['url'] = 'https:' + each_book.xpath('.//h4/a[@href and @data-bid]/@href')[0]
                book_info['name'] = each_book.xpath('.//h4/a[@href and @data-bid]/text()')[0]
                book_info['intro'] = each_book.xpath('.//p[@class="intro"]/text()')[0].strip()
                # 字数字体处理
                words_tags = each_book.xpath('.//p[@class="update"]/span')
                if words_tags:
                    words_style = words_tags[0].xpath('./style/text()')[0]
                    font_pattern = re.compile(r', url\(\'(.*?\.ttf)\'\)')
                    font_ttf_urls = re.findall(pattern=font_pattern, string=words_style)
                    if font_ttf_urls:
                        self._download_font(font_url=font_ttf_urls[0])
                        self.load_font()
                    # 原始的字数文本
                    raw_words = words_tags[0].xpath('./span[@class]/text()')
                    print(raw_words)
                print(book_info)

    def _download_font(self, font_url):
        """下载字体文件"""
        # 因为同一次主页请求中字体文件一致，所以只需下载一次
        if self.font_path is None:
            print(font_url)
            font_resp = requests.get(font_url)
            with open('temp_font.ttf', 'wb') as f:
                f.write(font_resp.content)
                self.font_path = 'temp_font.ttf'
        else:
            pass

    def load_font(self):
        font_table = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
                      'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
        if self.font_path is not None:
            font = TTFont(self.font_path)
            cmap = font.getBestCmap()
            print(cmap)


if __name__ == '__main__':
    qidian_spider = QidianSpider()
    qidian_spider.crawl()
