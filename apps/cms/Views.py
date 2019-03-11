# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:29
# Author  : LiaoKong

import string
import random

from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from flask_mail import Message

from .Forms import LoginForm, ResetPwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm
from .Models import CMSUser, CMSPermission
from ..Models import BannerModel
from .Decorators import login_required, permission_required

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
@login_required
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


@bp.route("/posts/")
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template("cms/cms_posts.html")


@bp.route("/comments/")
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template("cms/cms_comments.html")


@bp.route("/boards/")
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template("cms/cms_boards.html")


@bp.route("/fusers/")
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template("cms/cms_fusers.html")


@bp.route("/cusers/")
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template("cms/cms_cusers.html")


@bp.route("/croles/")
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template("cms/cms_croles.html")


@bp.route("/banners/")
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template("cms/cms_banners.html", banners=banners)


@bp.route("/abanner/", methods=["POST"])
@login_required
def abanner():
    form = AddBannerForm(request.form)

    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)

        db.session.add(banner)
        db.session.commit()

        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route("/ubanner/", methods=["POST"])
@login_required
def ubanner():
    form1 = UpdateBannerForm(request.form)

    if form1.validate():
        banner_id = form1.banner_id.data
        banner = BannerModel.query.get(banner_id)

        name = form1.name.data
        image_url = form1.image_url.data
        link_url = form1.link_url.data
        priority = form1.priority.data

        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority

            db.session.commit()

            return restful.success()
        else:
            return restful.params_error("没有这个轮播图！")
    else:
        restful.params_error(form1.get_error())


@bp.route("/dbanner/", methods=["POST"])
@login_required
def dbanner():
    banner_id = request.form.get("banner_id")

    if not banner_id:
        return restful.params_error(message="请传入轮播图id")

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message="没有这个轮播图")

    db.session.delete(banner)
    db.session.commit()

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
