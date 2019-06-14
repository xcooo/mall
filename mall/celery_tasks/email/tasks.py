#! /usr/bin/env python3
# encoding: utf-8
"""
@file: tasks.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from django.core.mail import send_mail
from django.conf import settings
from celery_tasks.main import app

@app.task(name='send_active_email')
def send_active_email(to_email, verify_url):
    """
     发送验证邮箱邮件
     :param to_email: 收件人邮箱
     :param verify_url: 验证链接
     :return: None
     """
    subject = "幸运商城邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用幸运商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)