# -*- coding: utf-8 -*-
# Time    : 2019/3/5 21:07
# Author  : LiaoKong

from flask import session, g

from .Views import bp
from .Models import CMSUser, CMSPermission

import Config


@bp.before_request
def before_request():
    if Config.CMS_USER_ID in session:
        user_id = session.get(Config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)

        if user:
            g.cms_user = user


@bp.context_processor
def cms_context_processor():
    return {"CMSPermission": CMSPermission}
