# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:36
# Author  : LiaoKong

from wtforms import StringField
from wtforms.validators import EqualTo, regexp, ValidationError

from utils import lkcache

from ..Forms import BaseForm
from .Models import FrontUser


class SignupForm(BaseForm):
    telephone = StringField(validators=[regexp(r"1[345789]\d{9}", message="请输入正确格式的手机号码")])
    sms_captcha = StringField(validators=[regexp(r"\w{4}", message="请输入正确格式的短信验证")])
    username = StringField(validators=[regexp(r".{2,20}", message="请输入正确格式的用户名")])
    password1 = StringField(validators=[regexp(r"[0-9a-zA-Z_\.]{6,20}", message="请输入正确格式的密码")])
    password2 = StringField(validators=[EqualTo("password1", message="两次输入的密码不一致")])
    graph_captcha = StringField(validators=[regexp(r"\w{4}", message="请输入正确格式的图形验证")])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data

        # fixme 1111仅用来测试 最后要删掉
        if sms_captcha != "1111":
            sms_captcha_mem = lkcache.get(telephone)
            if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
                raise ValidationError(message="短信验证码错误！")

    def validate_graph_captcha(self, field):
        graph_captcha = field.data

        graph_captcha_mem = lkcache.get(graph_captcha.lower())

        # fixme 1111仅用来测试 最后要删掉
        if graph_captcha != "1111":
            if not graph_captcha_mem:
                raise ValidationError(message="图形验证码错误！")

    def validate_telephone(self, field):
        telephone = field.data

        user = FrontUser.query.filter_by(telephone=telephone).first()

        if user:
            raise ValidationError(message="您所输入的电话已被注册！")


class SigninForm(BaseForm):
    telephone = StringField(validators=[regexp(r"1[345789]\d{9}", message="请输入正确格式的手机号码")])
    password = StringField(validators=[regexp(r"[0-9a-zA-Z_\.]{6,20}", message="请输入正确格式的密码")])
    remember = StringField()
