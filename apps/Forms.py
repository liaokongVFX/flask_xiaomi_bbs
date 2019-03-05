# -*- coding: utf-8 -*-
# Time    : 2019/3/5 23:12
# Author  : LiaoKong

from wtforms import Form


class BaseForm(Form):
    def get_error(self):
        # ("password",["请输入正确格式的密码"])
        return self.errors.popitem()[1][0]
