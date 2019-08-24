# -*- coding: utf-8 -*- 
# @Author : Leo

import requests

"""
秒拍视频APP

- Device: 华为Nova|HUAWEI CAZ-TL10
- OS: Android 7.0
- APP: 秒拍APP-V.7.1.19

请求参数加密 & 响应内容加密
- 请求头headers参数加密
  - cp_sign参数的生成方式
- 响应内容response加密
  - 需要将响应response二进制进行异或运算
"""


class MiaopaiApp:
    # APP版本号
    app_version = '7.1.19'
    # 评论列表获取url
    comment_url = 'http://b-api.ins.miaopai.com/2/comment/list.json?count={count}&page={page}&smid={smid}'
    # 请求头必需参数
    headers = {'cp_uuid': '', 'cp_ver': '', 'cp_sign': '', 'cp_time': '', 'Connection': 'close',
               'Host': 'b-api.ins.miaopai.com', 'User-Agent': 'okhttp/3.3.1', 'cp_os': 'android',
               'cp_channel': 'ppzhushou_market'}

    def __init__(self, video_id: str):
        self.video_id = video_id

    def get_video_info(self):
        """获取视频信息"""

    def get_video_comments(self):
        """获取视频评论"""
