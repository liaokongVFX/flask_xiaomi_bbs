# -*- coding: utf-8 -*-
# Time    : 2019/3/4 23:52
# Author  : LiaoKong

from functools import wraps

from flask import session, redirect, url_for

import Config


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if Config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("cms.login"))

    return inner
