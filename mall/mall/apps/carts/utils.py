#! /usr/bin/env python3
# encoding: utf-8
"""
@file: utils.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
import base64
import pickle

from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user, response):
    """
    合并请求用户的购物车数据，将未登录保存在cookie里的保存到redis中
    遇到cookie与redis中出现相同的商品时以cookie数据为主，覆盖redis中的数据
    1.商品数量: 以cookie为准
    2.勾选状态: 以cookie为准
    :param request: 用户的请求对象
    :param user: 当前登录的用户
    :param response: 响应对象，用于清楚购物车cookie
    :return:
    # 合并前
    redis_cart = {
        '1':10,
        '2':20,
        '3':30
    }
    redis_cart_selected = set(1,2,3)

    cookie_cart = {
        '1':{
            'count':10,
            'selected':False
        },
         '4':{
        'count':15,
        'selected':True
        }
    }

    # 合并后
    redis_cart = {
        '1':10,
        '2':20,
        '3':30,
        '4':'15
    }

    redis_cart_selected = set(2,3,4)
    """
    # 获取cookie中的购物车数据
    cookie_cart = request.COOKIES.get('cart')

    if not cookie_cart:
        return response

    # 表示cookie中有购物车数据
    # 解析
    cookie_cart_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))

    # 获取redis中购物车数据
    redis_conn = get_redis_connection('cart')
    redis_cart = redis_conn.hgetall('cart_%s' % user.id)

    # redis_cart = {
    #     商品sku_id  bytes字节类型 : 数量 bytes字节类型
    #     商品sku_id  bytes字节类型:  数量 bytes字节类型
    # }

    # 用来存储redis最终保存的商品数量信息的hash数据
    cart = {}
    for sku_id, count in redis_cart.items():
        cart[int(sku_id)] = int(count)

    # 用来记录redis最终操作时,哪些sku_id是需要勾选新增的
    redis_cart_selected_add = []

    # 用来记录redis最终操作时,哪些sku_id是需要取消勾选删除的
    redis_cart_selected_remove = []

    # 遍历cookie中的数据
    # cookie_cart_dict = {
    #   sku_id_1:
    #          { "count": 10,
    #          "selected": True},
    # }
    for sku_id, count_selected_dict in cookie_cart_dict.items():
        # 处理商品的数量, 维护在redis数量数据的最终字典
        cart[sku_id] = count_selected_dict['count']

        # 处理商品的勾选状态
        if count_selected_dict['selected']:
            # 如果cookie指明, 勾选
            redis_cart_selected_add.append(sku_id)
        else:
            # 如果cookie指明, 不勾选
            redis_cart_selected_remove.append(sku_id)

    if cart:
        # 执行redis操作
        pl = redis_conn.pipeline()

        # 设置hash类型
        pl.hmset('cart_%s' % user.id, cart)

        # 设置set类型
        if redis_cart_selected_add:
            pl.sadd('cart_select_%s' % user.id, *redis_cart_selected_add)

        if redis_cart_selected_remove:
            pl.srem('cart_select_%s' % user.id, *redis_cart_selected_remove)

        pl.execute()

    # 删除cookie
    response.delete_cookie('cart')
    return response
