# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:30
# Author  : LiaoKong

from flask import Blueprint

bp = Blueprint("front", __name__)


@bp.route("/")
def index():
    return "front index"

