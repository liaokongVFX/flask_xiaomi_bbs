# -*- coding: utf-8 -*-
# Time    : 2019/3/13 22:32
# Author  : LiaoKong

from flask import session, g, render_template

from .Views import bp
from .Models import FrontUser

import Config


@bp.before_request
def my_before_request():
    if Config.FRONT_USER_ID in session:
        user_id = session.get(Config.FRONT_USER_ID)
        user = FrontUser.query.get(user_id)

        if user:
            g.front_user = user


@bp.errorhandler
def page_not_found():
    return render_template("front/front_404.html"), 404
