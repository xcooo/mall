#! /usr/bin/env python3
# encoding: utf-8
"""
@file: seriaalizers.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from rest_framework import serializers
from django_redis import get_redis_connection

class ImageCodeCheckSerializer(serializers.Serializer):
    '''
    图片验证码序列化器
    :return
    '''
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        """
        反序列化校验
        """
        image_code_id = attrs['image_code_id']
        text = attrs['text']
        # 查询真实图片验证码
        redis_conn = get_redis_connection('verify_codes')
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)
        if not real_image_code_text:
            raise serializers.ValidationError('图片验证码无效')

        # 删除图片验证码
        redis_conn.delete('img_%s' % image_code_id)

        # 比较图片验证码
        real_image_code_text = real_image_code_text.decode()
        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError('图片验证码错误')

        # 判断是否在60s内
        # get_serializer 提供序列化器对象的时候,会补充context属性
        # context属性补充三个数据：request、format、view(类视图对象)，这三个数据对象可以在定义序列化器时使用。

        # django的类视图中, kwargs保存了路径提取出来的参数
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁')

        return attrs