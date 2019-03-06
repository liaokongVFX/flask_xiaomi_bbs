# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:29
# Author  : LiaoKong

import string
import random

from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from flask_mail import Message

from .Forms import LoginForm, ResetPwdForm, ResetEmailForm
from .Models import CMSUser
from .Decorators import login_required

import Config
from Exts import db, mail
from utils import restful, lkcache

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/")
@login_required
def index():
    return render_template("cms/cms_index.html")


@bp.route("/logout")
@login_required
def logout():
    del session[Config.CMS_USER_ID]
    return redirect(url_for("cms.login"))


@bp.route("/profile/")
@login_required
def profile():
    return render_template("cms/cms_profile.html")


@bp.route("/email_captcha/")
def email_captcha():
    email = request.args.get("email")

    if not email:
        return restful.params_error("请传递邮箱参数")

    # 生成验证码
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))

    message = Message("论坛邮箱验证码", recipients=[email], body="您的验证码是：%s" % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()

    lkcache.set(email, captcha)
    return restful.success()


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template("cms/cms_login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[Config.CMS_USER_ID] = user.id

                if remember:
                    # 过期时间为31天
                    session.permanent = True

                return redirect(url_for("cms.index"))
            else:
                return self.get(message="邮箱或密码错误")

        else:
            message = form.get_error()
            # ("password",["请输入正确格式的密码"])
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetpwd.html")

    def post(self):
        form = ResetPwdForm(request.form)

        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data

            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # {"code": 200, "message": ""}
                # return jsonify({"code": 200, "message": ""})
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetemail.html")

    def post(self):
        form = ResetEmailForm(request.form)

        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()

            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule("/login/", view_func=LoginView.as_view("login"))
bp.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view("resetpwd"))
bp.add_url_rule("/resetemail/", view_func=ResetEmailView.as_view("resetemail"))
