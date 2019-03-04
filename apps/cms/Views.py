# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:29
# Author  : LiaoKong

from flask import Blueprint

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/")
def index():
    return "cms index"
