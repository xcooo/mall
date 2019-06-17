#! /usr/bin/env python3
# encoding: utf-8
"""
@file: regenerate_index_html.py.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""

"""
功能：手动生成所有SKU的静态detail html文件
使用方法:
    ./regenerate_index_html.py
"""

import sys

sys.path.insert(0, '../')

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings.dev'

# 让django初始化设置
import django
django.setup()


from contents.crons import generate_static_index_html


if __name__ == '__main__':
    # 调用contents.crons  生成静态的主页html文件 方法
    generate_static_index_html()