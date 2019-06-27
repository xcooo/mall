#! /usr/bin/env python3
# encoding: utf-8
"""
@file: utils.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
import re

from django.contrib.auth.backends import ModelBackend
from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_account(account):
    """根据账号获取用户对象"""
    try:
        if re.match(r'^1[3-9]\d{9}$',account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """username可能是用户名,或者是手机号"""

        # 获取用户对象
        user =  get_user_by_account(username)

        # 校验用户是否存在 校验密码
        if user is not None and user.check_password(password):
            return user

