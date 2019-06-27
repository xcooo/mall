#! /usr/bin/env python3
# encoding: utf-8
"""
@file: urls.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    url(r'^users/$', views.UserView.as_view()),
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()), # 判断用户名
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),  # 判断手机号
    # url(r'^authorizations/$', obtain_jwt_token),  # JWT登录认证签发的路由
    url(r'^authorizations/$', views.UserAuthorizeView.as_view()),  # JWT登录认证签发的路由, 补充了合并购物车
    url(r'^user/$',views.UserDetailView.as_view()), # 个人中心基本信息
    url(r'^email/$',views.EmailView.as_view()),  # 保存邮箱并发送邮件
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),# 验证邮件
    url(r'^browse_histories/$', views.UserBrowsingHistoryView.as_view()) # 用户浏览历史记录
]

router = DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')

urlpatterns += router.urls

# POST /addresses/ 新建  -> create
# PUT /addresses/<pk>/ 修改  -> update
# GET /addresses/  查询  -> list
# DELETE /addresses/<pk>/  删除 -> destroy
# PUT /addresses/<pk>/status/ 设置默认 -> status
# PUT /addresses/<pk>/title/  设置标题 -> title