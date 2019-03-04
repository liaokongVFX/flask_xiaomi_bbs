# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:36
# Author  : LiaoKong

from wtforms import Form, StringField,IntegerField
from wtforms.validators import Email, InputRequired, Length


class LoginForm(Form):
    email = StringField(validators=[Email(message="请输入正确的邮箱格式"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(6, 20, message="请输入正确格式的密码")])
    remember = IntegerField()
