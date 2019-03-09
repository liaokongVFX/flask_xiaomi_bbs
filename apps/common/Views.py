# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:30
# Author  : LiaoKong

from io import BytesIO

from flask import Blueprint, request, make_response

from utils import restful, SmsSender, lkcache
from utils.captcha import xtcaptcha

from .Forms import SMSCaptchaForm

bp = Blueprint("common", __name__, url_prefix="/c")


# @bp.route("/sms_captcha/")
# def sms_captcha():
#     telephone = request.args.get("telephone")
#
#     if not telephone:
#         return restful.params_error(message="请传入手机号码！")
#
#     captcha = xtcaptcha.Captcha.gene_text()
#     if SmsSender.send(telephone, captcha):
#         return restful.success()
#     else:
#         restful.params_error(message="短信发送失败！")

@bp.route("/sms_captcha/", methods=["POST"])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data

        captcha = xtcaptcha.Captcha.gene_text()
        print("发送的短信验证码是 ", captcha)
        if SmsSender.send(telephone, captcha):
            # 保存短信验证码
            lkcache.set(telephone, captcha)
            return restful.success()
        else:
            # fixme 这里仅用作测试,最后要改回下面注销的代码
            lkcache.set(telephone, captcha)
            return restful.success()
            # return restful.params_error(message="短信发送失败！")

    else:
        return restful.params_error(message="参数错误！")


@bp.route("/captcha/")
def graph_captcha():
    # 获取验证码
    text, image = xtcaptcha.Captcha.gene_code()
    lkcache.set(text.lower(), text.lower())

    # BytesIO：字节流
    out = BytesIO()
    image.save(out, "png")
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = "image/png"
    return resp


if __name__ == '__main__':
    print(xtcaptcha.Captcha.gene_text())
