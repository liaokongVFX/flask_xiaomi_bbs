# -*- coding: utf-8 -*-
# Time    : 2019/3/9 20:36
# Author  : LiaoKong

import hashlib

from apps.Forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp, InputRequired


class SMSCaptchaForm(BaseForm):
    salt = "ljkdfjgdkfgdl;fddlcoss"
    telephone = StringField(validators=[regexp(r"1[345789]\d{9}")])
    timestamp = StringField(validators=[regexp(r"\d{13}")])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()

        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5需要穿一个bytes类似的字符串进去
        sign2 = hashlib.md5((telephone + timestamp + self.salt).encode("utf-8")).hexdigest()

        if sign == sign2:
            return True
        else:
            return False
