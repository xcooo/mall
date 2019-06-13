#! /usr/bin/env python3
# encoding: utf-8
"""
@file: main.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings.dev'


# 创建celery应用
app = Celery('meiduo')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 导入任务
app.autodiscover_tasks(['celery_tasks.sms'])


