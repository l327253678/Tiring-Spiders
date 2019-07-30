# -*- coding: utf-8 -*- 
# @Author : Leo

# coding=utf-8
'''
Created on 2018年8月23日
@author: Administrator
'''
import requests, json, time, re
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from fontTools.ttLib import TTFont
from io import BytesIO


start_url = 'https://www.qidian.com/finish?action=hidden&orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=2&page='


def get_font(url):
    response = requests.get(url)
    font = TTFont(BytesIO(response.content))
    cmap = font.getBestCmap()
    font.close()
    return cmap


def get_encode(cmap, values):
    WORD_MAP = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8',
                'nine': '9', 'period': '.'}
    word_count = ''
    for value in values.split(';'):
        value = value[2:]
        key = cmap[int(value)]
        word_count += WORD_MAP[key]
    return word_count


def get_index(start_url):
    # 获取当前页面的html
    response = requests.get(start_url).text
    doc = pq(response)
    # 获取当前字体文件名称
    classattr = doc('p.update > span > span').attr('class')
    pattern = '</style><span.*?%s.*?>(.*?)</span>' % classattr
    # 获取当前页面所有被字数字符
    numberlist = re.findall(pattern, response)
    # 获取当前包含字体文件链接的文本
    fonturl = doc('p.update > span > style').text()
    # 通过正则获取当前页面字体文件链接
    url = re.search('woff.*?url.*?\'(.+?)\'.*?truetype', fonturl).group(1)
    cmap = get_font(url)
    books = doc('.all-img-list li').items()
    i = 0
    for book in books:
        print(book)
        item = {}
        item['img'] = 'http:' + book('.book-img-box a img').attr('src')
        item['bookname'] = book('.book-mid-info h4 a').text()
        item['author'] = book('.name').text()
        item['classes'] = book('p.author > a:nth-child(4)').text()
        item['content'] = book('.intro').text()
        item['number'] = get_encode(cmap, numberlist[i][:-1])
        i += 1
        print(item)



def main():
    for page in range(1, 1000):
        url = start_url + str(page)
        get_index(url)


if __name__ == '__main__':
    main()
