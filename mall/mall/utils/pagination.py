#! /usr/bin/env python3
# encoding: utf-8
"""
@file: paginations.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    # 默认每页条数
    page_size =2

    # 前端指明访问参数名
    page_size_query_param = 'page_size'

    # 限制前端每页数量最大限制
    max_page_size = 20
