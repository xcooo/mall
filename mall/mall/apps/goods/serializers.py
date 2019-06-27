#! /usr/bin/env python3
# encoding: utf-8
"""
@file: serializers.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from rest_framework import serializers
from .models import SKU

from drf_haystack.serializers import HaystackSerializer
from .search_indexes import SKUIndex

class SKUSerializer(serializers.ModelSerializer):
    '''
    SKU商品序列化器
    '''
    class Meta:
        model = SKU
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')


class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """
    class Meta:
        index_classes = [SKUIndex]
        fields = ('text', 'id', 'name', 'price', 'default_image_url', 'comments')
