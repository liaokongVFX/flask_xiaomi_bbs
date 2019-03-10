# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:36
# Author  : LiaoKong

from flask import g

from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo

from ..Forms import BaseForm

from utils import lkcache


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱格式"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(6, 20, message="请输入正确格式的密码")])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message="请输入正确格式的旧密码")])
    newpwd = StringField(validators=[Length(6, 20, message="请输入正确格式的新密码")])
    newpwd2 = StringField(validators=[EqualTo("newpwd", message="确认密码必须和新密码保持一致")])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱格式"), InputRequired(message="请输入邮箱")])
    captcha = StringField(validators=[Length(min=6, max=6, message="请输入正确长度的验证码")])

    def validate_captcha(self, field):
        email = self.email.data
        captcha = field.data
        captcha_cache = lkcache.get(email)

        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError("邮箱验证码错误！")

    def validate_email(self, field):
        email = field.data
        user = g.cms_user

        if user.email == email:
            raise ValidationError("不能修改为相同的邮箱！")


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入轮播图名称")])
    image_url = StringField(validators=[InputRequired(message="请输入轮播图链接")])
    link_url = StringField(validators=[InputRequired(message="请输入轮播图跳转链接")])
    priority = IntegerField(validators=[InputRequired(message="请输入轮播图优先级")])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message="请输入轮播图id")])
