# -*- coding: utf-8 -*- 
# @Author : Leo


import re
import uuid
import time
import json
import requests
from urllib import parse
from hashlib import md5

"""
秒拍视频APP

- Device: 华为Nova|HUAWEI CAZ-TL10
- OS: Android 7.0
- APP: 秒拍APP-V.7.2.60

请求参数加密 & 响应内容加密
- 请求头headers参数加密
  - cp_sign参数的生成方式
- 响应内容response加密
  - 需要将响应response二进制进行异或运算
"""


class MiaopaiApp:
    # APP版本号
    app_version = '7.2.60'
    # 生成cp_sign的Key，定值
    const_key = '4O230P1eeOixfktCk2B0K8d0PcjyPoBC'
    # 视频信息获取url，其中smid即为视频id
    info_url = 'http://b-api.ins.miaopai.com/1/recommend/related.json?smid={smid}'
    # 评论列表获取url，其中smid即为视频id，count请求的评论条数，page页码数
    comment_url = 'http://b-api.ins.miaopai.com/2/comment/list.json?count={count}&page={page}&smid={smid}'

    def __init__(self, video_id: str):
        self.video_id = video_id
        # 请求头必需参数
        self.headers = {'cp_uuid': '', 'cp_ver': '', 'cp_sign': '', 'cp_time': '', 'Connection': 'close',
                        'Host': 'b-api.ins.miaopai.com', 'User-Agent': 'okhttp/3.3.1', 'cp_os': 'android',
                        'cp_channel': 'ppzhushou_market'}

    def get_video_info(self):
        """获取视频信息"""
        full_info_url = self.info_url.format(smid=self.video_id)
        self._set_headers(target_url=full_info_url)
        resp = requests.get(url=full_info_url, headers=self.headers)
        if not resp.ok:
            raise requests.exceptions.RequestException('视频信息响应状态码异常, status_code: %s' % resp.status_code)
        resp_text = self._decode_resp_content(resp_content=resp.content)
        print(resp_text)

    def get_video_comments(self):
        """获取视频评论"""
        pass

    def _set_headers(self, target_url: str) -> None:
        """设置请求headers
        cp_sign由URL路径、uuid、版本号、时间戳以及定值字符串key拼接后由md5加密生成
        :param target_url: 需要请求的目标URL
        :return:
        """

        # 获取cp_sign参数值
        def get_cp_sign():
            sign_raw_str = 'url=' + parse.urlparse(target_url).path + \
                           'unique_id=' + fake_uuid + \
                           'version=' + self.app_version + \
                           'timestamp=' + current_ts + \
                           self.const_key
            return md5((sign_raw_str.encode(encoding='utf-8'))).hexdigest()

        current_ts = str(int(time.time()))
        fake_uuid = str(uuid.uuid1())  # 伪造UUID，也叫做GUID(C#)
        self.headers['cp_ver'] = self.app_version
        self.headers['cp_time'] = current_ts
        self.headers['cp_uuid'] = fake_uuid
        self.headers['cp_sign'] = get_cp_sign()

    @staticmethod
    def _decode_resp_content(resp_content):
        """解密请求响应的数据"""

        def bytes_to_int(data, offset):
            result = 0
            for i in range(4):
                result |= (data[offset + i] & 0xff) << (8 * 1)
            return result

        def reverse_bytes(i):
            return ((i >> 24) & 0xFF) | ((i >> 8) & 0xFF00) | ((i << 8) & 0xFF0000) | (i << 24)

        if len(resp_content) <= 8:
            return ''
        dword0 = bytes_to_int(resp_content, 0)
        dword1 = bytes_to_int(resp_content, 4)
        x = 0
        if (dword0 ^ dword1) == -1936999725:
            x = reverse_bytes(dword1 ^ bytes_to_int(resp_content, 8))
        buffer_size = len(resp_content) - 12 - x
        if buffer_size <= 0:
            return ''
        else:
            buffer = bytearray()
            for index in range(buffer_size):
                buffer.append((resp_content[8 + index] ^ resp_content[12 + index]) & 0xff)
            return buffer.decode('utf8')


if __name__ == '__main__':
    test_video_id = 'C1U6Bq~RCnhkLJSsbwxxx1~B4zfWDI4d'
    spider = MiaopaiApp(video_id=test_video_id)
    spider.get_video_info()
    # spider.get_video_comments()
