# -*- coding: utf-8 -*-
# Time    : 2019/3/9 18:55
# Author  : LiaoKong

import requests

from Config import TPL_ID, SMS_KEY


def send(mobile, captcha):
    url = "http://v.juhe.cn/sms/send"
    params = {
        "mobile": mobile,
        "tpl_id": TPL_ID,
        "tpl_value": "#code#=" + captcha,
        "key": SMS_KEY
    }

    response = requests.get(url, params=params)
    result = response.json()

    if result["error_code"]:
        return False
    else:
        return True
