# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:30
# Author  : LiaoKong

from flask import Blueprint, views, render_template, request

from utils import restful,safeutils
from Exts import db

from .Forms import SignupForm
from .Models import FrontUser

bp = Blueprint("front", __name__)


@bp.route("/")
def index():
    return render_template("front/front_index.html")


@bp.route("/test/")
def test():
    return render_template("front/front_test.html")


class SignupView(views.MethodView):
    def get(self):
        # 获取跳转到这个页面之前的那个页面
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template("front/front_signup.html", return_to=return_to)
        else:
            return render_template("front/front_signup.html")

    def post(self):
        form = SignupForm(request.form)

        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()

            return restful.success()

        else:
            return restful.params_error(form.get_error())


bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))
