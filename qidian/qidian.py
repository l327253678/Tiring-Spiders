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

    # 字体映射
    font_cmap = None

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
                    # @font-face
                    words_style = words_tags[0].xpath('./style/text()')[0]
                    font_pattern = re.compile(r', url\(\'(.*?\.ttf)\'\)')
                    font_ttf_urls = re.findall(pattern=font_pattern, string=words_style)
                    if font_ttf_urls:
                        self._get_font(font_ttf_urls[0])
                    # 原始的字数文本
                    raw_words = words_tags[0].xpath('./span[@class]/text()')
                    self._get_true_value(fake_words=raw_words[0])
                print(book_info)

    def _get_font(self, font_url):
        """获取字体映射
        :param font_url: 字体url
        """
        font_resp = requests.get(font_url)
        # 因为同一次主页请求中字体文件一致，所以只需下载一次
        if self.font_cmap is None and font_resp.status_code == 200:
            font = TTFont(BytesIO(font_resp.content))
            self.font_cmap = font.getBestCmap()
            font.close()
        else:
            pass

    def _get_true_value(self, fake_words):
        """获取真实的字数"""
        font_table = {'period': '.', 'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
                      'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
        true_wrods_count = ''


if __name__ == '__main__':
    qidian_spider = QidianSpider()
    qidian_spider.crawl()
