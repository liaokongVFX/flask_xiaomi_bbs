# -*- coding: utf-8 -*-
# Time    : 2019/3/10 18:21
# Author  : LiaoKong

from datetime import datetime

from Exts import db


class BannerModel(db.Model):
    __tablename__ = "banner"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
