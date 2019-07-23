# -*- coding: utf-8 -*- 
# @Author : Leo

import hmac
import time
import base64
import hashlib
import requests
from urllib import parse

"""
豆瓣电影/图书/音乐

- Device: 华为Nova|HUAWEI CAZ-TL10
- OS: Android 7.0
- APP: 豆瓣V5.17.0(120)

# 检索URL示例
 - https://frodo.douban.com/api/v2/movie/tag?count=20&sort=U&q=%E7%94%B5%E5%BD%B1,%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&score_range=0,10&os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=360_Market&udid=30a998d6dfd04a47e581870cd56607f2b32df230&_sig=Ytzl9MpLm5OLnskufd/HwcpSKnQ%3D&_ts=1563848212
# 详情页URL示例
 - https://frodo.douban.com/api/v2/movie/26752088?loc_id=118281&os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=360_Market&udid=30a998d6dfd04a47e581870cd56607f2b32df230&_sig=ba75TdcR2r4l2kleTO3Ljl3rZx8%3D&_ts=1563848268

# 目标: 解决URL中sign参数的生成方式
"""

# API_SECRET_KEY和API_KEY抓包多个设备，两者值为常量
API_SECRET_KEY = '9e8bb54dc3288cdf'
API_KEY = '0dad551ec0f84ed02907ff5c42e8ec70'
# 完整UA值包括设备UA+型号+网络等信息，只取APP版本标识即可
# api-client/1 com.douban.frodo/5.17.0(120) Android/24 product/CAZ-TL10 vendor/HUAWEI model/HUAWEI CAZ-TL10  rom/android  network/wifi
USER_AGENT = 'api-client/1 com.douban.frodo/5.17.0(120)'

# 影视数据列表接口
video_list_api = 'https://frodo.douban.com/api/v2/movie/tag'
# 影视数据接口参数
# start: 检索游标
# count: 单页返回数据条数，默认20，最大50
# sort: 排序方式 U默认 T热度 S评分 R时间
# q: 检索关键词，检索年代
# score_range: 影视评分
# apikey: 定值，更换手机设备也不会变
# _sig: 由api_secret_key+请求方法+请求链接+_ts组合sha1加密生成
search_params = {
    'start': 0,
    'count': 20,
    'sort': 'U',
    'q': '',
    'score_range': '',
    'os_rom': 'android',
    'apikey': API_KEY,
    'channel': '360_Market',
    '_sig': '',
    '_ts': ''}


def gen_sign(url: str, ts: int, method='GET') -> str:
    """请求URL_sign参数生成方式
    :param url: 需要请求的URL
    :param ts: 时间戳，可伪造
    :param method: 请求方法
    :return:
    """
    url_path = parse.urlparse(url).path
    raw_sign = '&'.join([method.upper(), parse.quote(url_path, safe=''), str(ts)])
    return base64.b64encode(hmac.new(API_SECRET_KEY.encode(), raw_sign.encode(), hashlib.sha1).digest()).decode()


def get_full_url(kw, start=0):
    """获取完整的关键词检索URL
    :param kw: 检索关键词
    :param start: 检索游标
    """
    params = search_params.copy()
    params['start'] = start
    params['q'] = kw
    params['score_range'] = '0,10'  # 评分区间
    cur_ts = int(time.time())
    params['_sig'] = gen_sign(url=video_list_api, ts=cur_ts)
    params['_ts'] = cur_ts
    return video_list_api + '?' + parse.urlencode(params, safe=',')


def start_search(keyword):
    """检索入口
    :param keyword: 检索关键词"""
    search_url = get_full_url(kw=keyword)
    headers = {'User-Agent': USER_AGENT}
    resp = requests.get(url=search_url, headers=headers)
    print('请求响应状态码:', resp.status_code)
    print('请求响应内容:', resp.text)


if __name__ == '__main__':
    # 用于测试的检索关键词
    test_kw = '电影'
    start_search(test_kw)
