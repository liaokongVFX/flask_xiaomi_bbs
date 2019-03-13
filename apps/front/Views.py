# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:30
# Author  : LiaoKong

from flask import Blueprint, views, render_template, request, session, url_for

from utils import restful, safeutils
from Exts import db
import Config

from .Forms import SignupForm, SigninForm, AddPostForm
from .Models import FrontUser
from ..Models import BannerModel, BoardModel, PostModel
from .Decorators import login_required

bp = Blueprint("front", __name__)


@bp.route("/")
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    context = {
        "banners": banners,
        "boards": boards
    }

    return render_template("front/front_index.html", **context)


@bp.route("/apost/", methods=["GET", "POST"])
@login_required
def apost():
    if request.method == "GET":
        boards = BoardModel.query.all()
        return render_template("front/front_apost.html", boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data

            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message="没有这个版块")

            post = PostModel(title=title, content=content)
            post.board = board
            db.session.add(post)
            db.session.commit()

            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


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


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(
                return_to):
            return render_template("front/front_signin.html", return_to=return_to)
        else:
            return render_template("front/front_signin.html")

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[Config.FRONT_USER_ID] = user.id

                if remember:
                    # session为31天
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message="手机号或者密码错误")
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))
bp.add_url_rule("/signin/", view_func=SigninView.as_view("signin"))
