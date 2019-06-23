#! /usr/bin/env python3
# encoding: utf-8
"""
@file: db_router.py.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
class MasterSlaveDBRouter(object):
    """数据库主从读写分离路由"""

    def db_for_read(self, model, **hints):
        """读数据库"""
        return "slave"

    def db_for_write(self, model, **hints):
        """写数据库"""
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return True