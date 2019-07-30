# -*- coding: utf-8 -*- 
# @Author : Leo

import time
import random
import requests
from hashlib import md5
from urllib.parse import quote, unquote_plus, urlencode

"""
美拍视频

- Device: 华为Nova|HUAWEI CAZ-TL10
- OS: Android 7.0
- APP: 美拍V7700

请求参数加密
- sig参数的生成
- 获取视频信息与评论的sign生成方式一致
"""


class MeipaiApp:
    """根据视频ID采集其视频信息以及评论列表"""

    # 视频信息api
    video_base_api = 'https://api.meipai.com/medias/show.json'
    # 评论列表api
    comment_base_api = 'https://api.meipai.com/comments/show.json'
    # headers
    common_header = {'User-Agent': ''}

    def __init__(self, video_id):
        self.video_id = video_id
        # 视频信息参数
        self.video_info_params = {
            'id': '1102848496', 'language': 'zh-Hans', 'client_id': '1089857302', 'version': '7700',
            'channel': 'meipai_alic', 'origin_channel': 'meipai_alic', 'locale': '1',
            'mac': '02%3A00%3A00%3A00%3A00%3A00', 'stat_gid': '1786894244', 'network': 'wifi',
            'sig': 'c84a30988714233e3ed4b726593d63d2', 'sigVersion': '1.3', 'sigTime': '1555559856284'}
        # 视频评论列表参数
        self.comments_params = {
            'id': '1101452728', 'language': 'zh-Hans', 'client_id': '1089857302', 'device_id': '862206032375701',
            'version': '7700', 'channel': 'meipai_alic', 'origin_channel': 'meipai_alic', 'locale': '1',
            'iccid': '89860118841819543585', 'imei': '862206032375701', 'mac': '02%3A00%3A00%3A00%3A00%3A00',
            'network': 'wifi', 'sig': '44749e22b4a1067d5b90be8fcdf21367', 'sigVersion': '1.3', 'sigTime': '1555551739398'}

    def get_video_info(self):
        """获取视频信息"""
        video_info_url = self._get_video_url()
        print('视频信息完整URL->', video_info_url)
        video_resp = requests.get(url=video_info_url, headers={'User-Agent': 'okhttp/3.10.0'})
        if video_resp.status_code == 200:
            return video_resp.json()
        else:
            return None

    def get_video_comments(self):
        """获取视频评论列表"""
        comments_url = self._get_comment_url(max_id='')
        print('评论列表完整URL->', comments_url)
        # TODO 示例中只获取了首页评论
        comment_resp = requests.get(url=comments_url, headers={'User-Agent': 'okhttp/3.10.0'})
        if comment_resp.status_code == 200:
            return comment_resp.json()
        else:
            return None

    def _get_video_url(self):
        """获取视频信息url"""
        self.video_info_params['id'] = self.video_id
        # 伪造mac地址
        self.video_info_params['mac'] = self._get_fake_mac()
        self.video_info_params['sigTime'] = str(int(time.time() * 1000))
        self.video_info_params['sig'] = self._get_sig(self.video_info_params)
        return self.video_base_api + '?' + urlencode(self.video_info_params)

    def _get_comment_url(self, max_id=''):
        """获取comment列表
        :param max_id: 评论ID游标
        """
        self.comments_params['id'] = self.video_id
        self.comments_params['max_id'] = max_id
        # 伪造imei
        self.comments_params['imei'] = str(random.randint(100000000000000, 300000000000000))
        # 伪造mac地址
        self.comments_params['mac'] = self._get_fake_mac()
        self.comments_params['sigTime'] = str(int(time.time() * 1000))
        # 伪造设备ID
        self.comments_params['device_id'] = str(random.randint(862200032375701, 862209032375701))
        sig_str = self._get_sig(url_params=self.comments_params, url_type='comments/show.json')
        self.comments_params['sig'] = sig_str
        return self.comment_base_api + '?' + urlencode(self.comments_params)

    @staticmethod
    def _get_fake_mac():
        temp_mac_string = '0123456789abcdef'
        target_mac = ''
        for _ in range(12):
            target_mac += random.choice(temp_mac_string)
        return ':'.join([target_mac[i] + target_mac[i + 1] for i in range(len(target_mac)) if i % 2 == 0])

    @staticmethod
    def _get_sig(url_params: dict, url_type='medias/show.json') -> str:
        """获取sig值，`url路由+url参数+常量字符串+sigTime+常量字符串`后进行md5加密
        :param url_params: URL参数列表
        :param url_type: URL类型路由，默认是获取视频信息
        :return:
        """
        params_values = [unquote_plus(v) for k, v in url_params.items() if 'sig' not in k]
        params_values.sort()
        encry_params_str = url_type + ''.join(params_values) + 'bdaefd747c7d594f' + url_params['sigTime'] + 'Tw5AY783H@EU3#XC'
        params_md5_str = md5(encry_params_str.encode(encoding='utf-8')).hexdigest()
        params_md5_list = list(params_md5_str)
        for i in range(len(params_md5_str)):
            if i % 2 == 0:
                params_md5_list[i], params_md5_list[i + 1] = params_md5_list[i + 1], params_md5_list[i]
        return ''.join(params_md5_list)


if __name__ == '__main__':
    t_video_id = '1128279673'
    spider = MeipaiApp(video_id=t_video_id)
    info = spider.get_video_info()
    print('视频信息->', info)
    comments = spider.get_video_comments()
    print('评论列表->', comments)
