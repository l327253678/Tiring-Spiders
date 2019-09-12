# -*- coding: utf-8 -*- 
# @Author : Leo


import json
import time
import uuid
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

"""
花生头条APP

正文内容获取，根据web-js流程提取
AES对称加密
"""


class HuashengToutiao:
    """花生头条APP"""

    def __init__(self, board_info):
        # 板块请求信息
        self.board_info = board_info
        # AES加密key，定值
        self.aes_key = 'G8BzJQSb7ZkNYKQnr5haZM8O'
        # CBC模式偏移量，定值
        self.iv = '0000000000000000'
        # 新闻列表页和正文URL
        self.news_url = 'https://news-api.xcmad.com/news/public/securityApiHandler.do'
        # 请求头
        self.headers = {'Content-Type': 'text/plain;charset=utf-8'}
        # 正文数据未加密提交数据
        self.content_data_format = {
            'body': {
                'id': '0ff0bfa5-f18c-4dd5-9df2-d661b2aa10af'},
            'header': {
                'action': 202,
                'appVersion': 100,
                'cmdName': 'app_h5',
                'phoneName': 'android',
                'platformCode': 'Android',
                'platformVersion': '4.0',
                'traceID': 'h5-1568275124205',
                'token': '',
                'userId': '',
                'uuid': 'h5835017521957362'}}

    def get_news_contents(self):
        """获取新闻列表"""
        # 将提交的板块信息序列化
        board_str = json.dumps(self.board_info)
        board_encrypt_str = self._aes_encrypt(text=board_str)
        # 获取新闻列表
        board_resp = requests.post(url=self.news_url, data=board_encrypt_str, headers=self.headers)
        if board_resp.ok:
            # 列表页数据
            pages_data = board_resp.json()
            if isinstance(pages_data, dict) and pages_data.get('code') == 0:
                news_items = pages_data.get('data')
                return [self.get_news_detail(news_id=item.get('unid')) for item in news_items]
        return []

    def get_news_detail(self, news_id: str):
        """获取单个新闻正文数据
        :param news_id: 新闻ID"""
        content_submit = self.content_data_format.copy()
        content_submit['body']['id'] = news_id
        # h5-毫秒时间戳
        content_submit['header']['traceID'] = 'h5-' + str(int(time.time() * 1000))
        # 随机生成的16位字符串
        content_submit['header']['uuid'] = 'h' + str(uuid.uuid1().int)[:16]
        detail_str = json.dumps(content_submit)
        detail_encrypt_str = self._aes_encrypt(text=detail_str)
        try:
            # 获取新闻详情页
            detail_resp = requests.post(url=self.news_url, data=detail_encrypt_str, headers=self.headers)
            if detail_resp.ok:
                detail_data = detail_resp.json()
                if isinstance(detail_data, dict) and detail_data.get('code') == 0:
                    return detail_data.get('data')
        except requests.exceptions.RequestException:
            print('请求新闻详情页出错')
        return None

    def _aes_decrypt(self, text):
        """aes解密"""
        pass

    def _aes_encrypt(self, text):
        """aes加密
        :param text: 明文字符串"""
        aes = AES.new(self.aes_key.encode(), AES.MODE_CBC, iv=self.iv.encode())
        # 选择pkcs7补全
        pad_pkcs7 = pad(text.encode('utf-8'), AES.block_size, style='pkcs7')
        aes_encrypt_ = aes.encrypt(pad_pkcs7)
        return base64.b64encode(aes_encrypt_).decode()


if __name__ == '__main__':
    from prettyprinter import cpprint

    # 以推荐板块为例测试
    temp_board = {
        'header': {
            'platformVersion': '8.1.0',
            'platformCode': 'Android',
            'cmdName': 'app360',
            'token': '',
            'appVersion': '1.4.8',
            'uuid': '868661030024913',
            'ts': 1566381935556,
            'traceID': 'A20190821180535033688',
            'action': '212',
            'phoneName': 'Xiaomi_Redmi 5A',
            'package': 'com.xcm.huasheng'},
        'body': {
            'category': '0,21,10,22,12,6,7,20,3',
            'gender': '1'}
    }
    spider = HuashengToutiao(board_info=temp_board)
    result = spider.get_news_contents()
    cpprint(result)
