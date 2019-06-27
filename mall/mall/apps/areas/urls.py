#! /usr/bin/env python3
# encoding: utf-8
"""
@file: urls.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [

]

router = DefaultRouter()
router.register('areas', views.AreasViewSet, base_name='areas')

urlpatterns += router.urls

# GET /areas/  {"get":"list"}  返回顶级数据  parent = None

# GET /areas/<pk>  {"get":"retrieve"}