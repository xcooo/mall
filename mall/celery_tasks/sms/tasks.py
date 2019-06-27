#! /usr/bin/env python3
# encoding: utf-8
"""
@file: tasks.py
@author: www.xcooo.cn
@Mail: 602006050@qq.com
"""
from .utils.yuntongxun.sms import CCP
import logging
from celery_tasks.main import app

logger = logging.getLogger('django')

# 验证码短信模板
SMS_CODE_TEMP_ID = 1

@app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, expires):
    '''
    celery发送短信验证码
    :return:
    '''
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [sms_code, expires], SMS_CODE_TEMP_ID)
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
