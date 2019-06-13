#! /usr/bin/env python3
# encoding: utf-8
"""
@file: constants.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""

# 此处存放常量

# 图片验证码过期时间,单位为秒
IMAGE_CODE_REDIS_EXPIRES = 5 * 60

# 短信验证码过期时间
SMS_CODE_REDIS_EXPIRES = 5 * 60

# 短信发送记录
SEND_SMS_CODE_INTERVAL = 1 * 60

# 短信验证码信息模板
SMS_CODE_TEMP_ID = 1