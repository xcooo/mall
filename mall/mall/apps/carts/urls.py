#! /usr/bin/env python3
# encoding: utf-8
"""
@file: urls.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cart/$', views.CartView.as_view()),
    url(r'^cart/selection/$', views.CartSelectAllView.as_view())
]

