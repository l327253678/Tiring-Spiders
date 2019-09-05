# -*- coding: utf-8 -*- 
# @Author : Leo

import uuid
import hmac
import time
import base64
import hashlib
import requests

"""
触电新闻
- https://www.itouchtv.cn/index

请求headers中存在加密参数
- X-ITOUCHTV-Ca-Signature: 将请求方法/目标地址/时间戳/空字符串由换行符拼接后，通过sha256生成摘要，再进行base64加密得到

eg:
  X-ITOUCHTV-Ca-Key: 28778826534697375418351580924221
  X-ITOUCHTV-Ca-Signature: 0fbNgqOkkWx/a1xmfoybmaq6PxPkFDZWlQ1r9Vdtsyw=
  X-ITOUCHTV-Ca-Timestamp: 1567650431295
  X-ITOUCHTV-CLIENT: ITOUCHTV_WEB
  X-ITOUCHTV-DEVICE-ID: WEB_b69027b0-cef9-11e9-beed-23bc5b95245b
"""

# 加密定值key
CONST_KEY = 'HGXimfS2hcAeWbsCW19JQ7PDasYOgg1lY2UWUDVX8nNmwr6aSaFznnPzKrZ84VY1'


def get_headers(target_url: str, ts_ms: int, method: str = 'GET') -> dict:
    """获取请求headers
    :param target_url: 目标url
    :param ts_ms: 当前毫秒时间戳
    :param method: 请求方法，默认GET"""
    message_text = '\n'.join([method, target_url, str(ts_ms), ''])
    # 先进行
    hmac_obj = hmac.new(key=CONST_KEY.encode(), msg=message_text.encode(), digestmod=hashlib.sha256)
    signature = base64.b64encode(hmac_obj.digest()).decode()
    cur_headers = {
        'X-ITOUCHTV-Ca-Key': '28778826534697375418351580924221',
        'X-ITOUCHTV-Ca-Signature': signature,
        'X-ITOUCHTV-Ca-Timestamp': str(ts_ms),
        'X-ITOUCHTV-CLIENT': 'ITOUCHTV_WEB',
        'X-ITOUCHTV-DEVICE-ID': 'WEB_' + str(uuid.uuid1())
    }
    return cur_headers


def get_recommend_news():
    """获取新闻推荐列表"""
    # 触电新闻主页推荐实际URL
    recommend_news_url = 'https://api.itouchtv.cn:8090/newsservice/v9/recommendNews?size=24&channelId=0'
    # 当前毫秒时间戳
    current_ms = int(time.time() * 1000)
    headers = get_headers(target_url=recommend_news_url, ts_ms=current_ms)
    resp = requests.get(url=recommend_news_url, headers=headers)
    if resp.ok:
        news_data = resp.json()
        return news_data.get('newsList', [])
    else:
        raise Exception('请求异常:\n==> target_url: %s\n==> headers: %s' % (recommend_news_url, headers))


if __name__ == '__main__':
    # 以获取推荐页为例，也适用于其它版块
    result = get_recommend_news()
    print('新闻列表 >>', result)
