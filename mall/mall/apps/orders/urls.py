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
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view()), # 订单结算
    url(r'^orders/$', views.SaveOrderView.as_view()), # 保存订单
]

