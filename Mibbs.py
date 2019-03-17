# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:24
# Author  : LiaoKong

from flask import Flask
from flask_wtf import CSRFProtect

from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from apps.ueditor import bp as ueditor_bp

import Config
from Exts import db, mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(ueditor_bp)

    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)

    return app


app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run()
