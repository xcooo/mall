#! /usr/bin/env python3
# encoding: utf-8
"""
@file: utils.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
import json

from django.conf import settings
import urllib.parse
from urllib.request import urlopen
import logging
from .exceptions import OAuthQQAPIError
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer,BadData
from . import constants

logger = logging.getLogger('django')

class OAuthQQ(object):
    """
    QQ认证辅助工具类
    """
    def __init__(self, client_id=None, redirect_url=None, state=None, client_secret=None):
        self.client_id = client_id if client_id else settings.QQ_CLIENT_ID
        self.redirect_uri = redirect_url if redirect_url else settings.QQ_REDIRECT_URI
        # self.state = state if state else settings.QQ_STATE
        self.state = state or settings.QQ_STATE  # 用于保存登录成功后的跳转页面路径
        self.client_secret = client_secret if client_secret else settings.QQ_CLIENT_SECRET

    # 获取qq登陆的url
    def get_login_url(self):
        # 请求地址
        url = 'https://graph.qq.com/oauth2.0/authorize?'

        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
        }

        url += urllib.parse.urlencode(params)

        return url

    # 获取 access_token
    def get_access_token(self, code):
        # 请求地址
        url = 'https://graph.qq.com/oauth2.0/token?'

        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        url += urllib.parse.urlencode(params)

        try:
            # 携带code 向qq服务器请求 access_token
            resp = urlopen(url)
            # 读取响应体数据
            resp_data = resp.read()  # bytes
            resp_data = resp_data.decode()  # str

            # access_token = FE04 ** ** ** ** ** ** ** ** ** ** ** ** CCE2 & expires_in = 7776000 & refresh_token = 88E4 ** ** ** ** ** ** ** ** ** ** ** ** BE14

            # 解析 access token
            resp_dict = urllib.parse.parse_qs(resp_data)
        except Exception as e:
            logger.error('获取access_token异常: %s' % e)
            raise OAuthQQAPIError
        else:
            access_token = resp_dict.get('access_token')

            return access_token[0]

    # 通过access token 获取 openid
    def get_openid(self, access_token):
        # 请求地址
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token

        try:
            # 携带access token 向qq服务器请求 openid
            resp = urlopen(url)
            # 读取响应体数据
            resp_data = resp.read()  # bytes
            resp_data = resp_data.decode()  # str

            # callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );

            # 解析 openid
            resp_data = resp_data[10:-4]
            resp_dict = json.loads(resp_data)
        except Exception as e:
            logger.error('获取openid异常: %s' % e)
            raise OAuthQQAPIError
        else:
            openid = resp_dict.get('openid')

            return openid

    # 用户是第一次使用QQ登录时返回，其中包含openid，用于绑定身份使用，注意这个access token是我们自己生成的
    # 使用itsdangerous生成凭据access_token
    def generate_bind_access_token(self, openid):
        serializer = TJWSSerializer(settings.SECRET_KEY, constants.BIND_USER_ACCESS_TOKEN_EXPIRES)
        token = serializer.dumps({'openid':openid})
        token = token.decode()
        return token

    # 检验token
    # 验证失败，会抛出itsdangerous.BadData异常
    @staticmethod
    def check_bind_access_token(access_token):
        serializer = TJWSSerializer(settings.SECRET_KEY, constants.BIND_USER_ACCESS_TOKEN_EXPIRES)
        try:
            data = serializer.loads(access_token)
        except BadData:
            return None
        else:
            return data['openid']