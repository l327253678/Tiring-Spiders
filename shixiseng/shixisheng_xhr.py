# -*- coding: utf-8 -*- 
# @Author : Leo

import time
import random
import requests
from urllib import parse
from fontTools.ttLib import TTFont
from prettyprinter import cpprint

# 首页URL
home_url = 'https://www.shixiseng.com/'
# 检索链接和参数
search_base_url = 'https://www.shixiseng.com/app/interns/search/v2'
search_params = {
    'build_time': '13位时间戳',
    'page': 1,
    'keyword': '关键词',
    'type': 'intern',
    'sortType': '',
    'city': '城市',
    'internExtend': ''}

# 加密字体下载链接
font_url = f'https://www.shixiseng.com/interns/iconfonts/file?rand={random.random()}'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'referer': 'https://www.shixiseng.com/gz'
}
# 字体文件保存路径
font_path = 'shixiseng.woff'

# 下载字体文件
try:
    font_resp = requests.get(url=font_url, headers=headers)
    if font_resp.status_code == 200:
        with open(font_path, 'wb') as f:
            f.write(font_resp.content)
except requests.exceptions.RequestException:
    raise requests.exceptions.RequestException('请求下载字体文件失败')


def get_font_map():
    """构建字体映射
    TODO 暴力强制转换"""
    font = TTFont(font_path)
    # font.saveXML('shixiseng.xml')
    cmap = font.getBestCmap()
    raw_font_map = dict()
    for k, v in cmap.items():
        # 将k转换成16进制可得到0x的实际值
        trans_k = hex(k)
        trans_v = v.replace('uni', '')
        raw_font_map[trans_k] = 'u' + '0' * (4 - len(trans_v)) + trans_v
    raw_font_map.pop('0x78')
    # 转换成unicode
    unicode_font_map = {i: eval('u' + '\'\\' + j + '\'') for i, j in raw_font_map.items()}
    return {k.replace('0x', '&#x'): v for k, v in unicode_font_map.items()}


font_map = get_font_map()
print('自定义字体映射字典>>')
print(font_map)


def trans_raw_data(data):
    """转换原始数据中加密的字体"""

    def raw_to_real(raw: str):
        if '&#x' in raw:
            chars = raw.split('&#x')
            char_list = []
            for c in chars:
                if c.isalnum() and '&#x' + c in font_map:
                    char_list.append(font_map.get('&#x' + c))
                else:
                    char_list.append(c)
            return ''.join(char_list)
        return raw

    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = raw_to_real(v)
            elif isinstance(v, dict) or isinstance(v, list):
                trans_raw_data(data=v)
            else:
                pass
    elif isinstance(data, list):
        for item in data:
            trans_raw_data(item)


def get_page_items(keyword: str, city: str, page=1):
    """获取当前页所有的数据"""
    params = search_params.copy()
    params['keyword'] = keyword
    params['city'] = city
    params['page'] = page
    params['build_time'] = int(time.time() * 1000)
    full_search_url = search_base_url + '?' + parse.urlencode(params)
    print('检索完整URL>>\n', full_search_url)
    resp = requests.get(url=full_search_url, headers=headers)
    if resp.ok:
        page_data = resp.json()
        # 处理json数据中的加密字体
        trans_raw_data(page_data)
        # print('处理字体后得到的json数据>>')
        # cpprint(page_data)
        return page_data
    else:
        raise requests.exceptions.RequestException('请求检索URL出错')


if __name__ == '__main__':
    temp_kw = 'Python'
    temp_city = '广州'
    search_result = get_page_items(keyword=temp_kw, city=temp_city)
    print('检索结果>>')
    cpprint(search_result)
