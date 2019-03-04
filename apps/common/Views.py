# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:30
# Author  : LiaoKong

from flask import Blueprint

bp = Blueprint("common", __name__, url_prefix="/common")


@bp.route("/")
def index():
    return "common index"

