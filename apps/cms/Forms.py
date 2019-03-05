# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:36
# Author  : LiaoKong

from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo

from ..Forms import BaseForm


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱格式"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(6, 20, message="请输入正确格式的密码")])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message="请输入正确格式的旧密码")])
    newpwd = StringField(validators=[Length(6, 20, message="请输入正确格式的新密码")])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message="确认密码必须和新密码保持一致")])
