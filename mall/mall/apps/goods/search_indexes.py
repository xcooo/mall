#! /usr/bin/env python3
# encoding: utf-8
"""
@file: search_indexes.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from haystack import indexes

from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SKU索引数据模型类
    """
    # 作用:
    # 1.明确搜索引擎索引数据包含哪些字段
    # 2.字段也会作为前端检索查询时关键词的参数名
    text = indexes.CharField(document=True, use_template=True)

    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.DecimalField(model_attr='price')
    default_image_url = indexes.CharField(model_attr='default_image_url')
    comments = indexes.IntegerField(model_attr='comments')

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        # return  SKU.objects.filter(is_launched=True)
        return self.get_model().objects.filter(is_launched=True)
