# -*- coding: utf-8 -*-
# Time    : 2019/3/4 21:26
# Author  : LiaoKong

import os

# fixme 最后要把注释掉的改回来
# SECRET_KEY = os.urandom(24)
SECRET_KEY = "dfklgjdfgkdfgldfvcdrdelxxx"

DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'mibbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = "cms_user_id"
FRONT_USER_ID = "front_user_id"

# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True
# MAIL_USE_SSL : default False
MAIL_USERNAME = "568250549@qq.com"
MAIL_PASSWORD = "zwd6666666666fcb"
MAIL_DEFAULT_SENDER = "568250549@qq.com"

# 短信验证码
TPL_ID = "140894"
SMS_KEY = "338c96ba3a666666666691d34b16a6c6"

# 七牛
QININ_ACCESS_KEY = "H_3SSw90-Z2fg6666666666666666QBsfQKjHm55"
QININ_SECRET_KEY = "H3rnY1YHpMGMz6666666666666666gY56hgzG3Ez"
QININ_BUCKET = "mibbs"

# 七牛ueditor上传
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "H_3SSw90-Z2fg6666666666666666QBsfQKjHm55"
UEDITOR_QINIU_SECRET_KEY = "H3rnY1YHpMGMz6666666666666666gY56hgzG3Ez"
UEDITOR_QINIU_BUCKET_NAME = "mibbs"
UEDITOR_QINIU_DOMAIN = "http://po7fr1krl.bkt.clouddn.com/"

# flask-paginate
PER_PAGE = 10


# celery 相关配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
