# -*- coding: utf-8 -*-
# Time    : 2019/3/5 23:27
# Author  : LiaoKong

from flask import jsonify


class HttpCode(object):
    ok = 200
    params_error = 400
    unauth_error = 401
    server_error = 500


def restful_result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data or {}})


def success(message="", data=None):
    return restful_result(HttpCode.ok, message, data)


def unauth_error(message=""):
    return restful_result(HttpCode.unauth_error, message, None)


def params_error(message=""):
    return restful_result(HttpCode.params_error, message, None)


def server_error(message=""):
    return restful_result(HttpCode.params_error, message or "服务器内部错误", None)
