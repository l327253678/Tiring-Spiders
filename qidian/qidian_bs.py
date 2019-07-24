# -*- coding: utf-8 -*-
# @Author : Leo

import re
import requests
from io import BytesIO
from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup


class QidianSpider:
    """起点中文网-字体反爬"""
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
            soup = BeautifulSoup(resp.text, 'html.parser')
            # books_content = soup.find_all('div', {'class': 'all-book-list'})
            book_infos = soup.find_all('div', {'class': 'book-mid-info'})
            for book in book_infos:
                book_info = dict()
                # 为展现反爬，所以只提取了标题和字数两项
                # 提取小说标题，
                book_info['title'] = book.find('h4').get_text()
                # 提取字数
                update_tag = book.find('p', {'class': 'update'})
                r = update_tag.find_all('span')
                for i in r:
                    print(i)


if __name__ == '__main__':
    qidian_spider = QidianSpider()
    qidian_spider.crawl()
