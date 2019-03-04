# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:29
# Author  : LiaoKong

from flask import Blueprint, views, render_template, request, session, redirect, url_for

from .Forms import LoginForm
from .Models import CMSUser
from .Decorators import login_required

import Config

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/")
@login_required
def index():
    return render_template("cms/cms_index.html")


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
            message = form.errors.popitem()[1][0]
            return self.get(message=message)


bp.add_url_rule("/login/", view_func=LoginView.as_view("login"))
