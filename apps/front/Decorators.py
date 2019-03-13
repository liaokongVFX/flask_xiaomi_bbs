# -*- coding: utf-8 -*-
# Time    : 2019/3/13 21:45
# Author  : LiaoKong

from functools import wraps

from flask import session, redirect, url_for

import Config


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if Config.FRONT_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("front.signin"))

    return inner
