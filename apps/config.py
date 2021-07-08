# -*- coding: utf-8 -*-
import os

file_path = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Base configuration"""
    SECRET_KEY = "5f3523l9324cy2463s51387a0aec5d2f"

    # db
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql123321@192.168.9.102:33306/test_plarform'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Api文档
    API_DOC_MEMBER = ['api_blueprint']  # 需要显示文档的API
    RESTFUL_API_DOC_EXCLUDE = []  # 需要排除文档的API

    # celery
    CELERY_RESULT_BACKEND = 'redis://:npUvCrC3@127.0.0.1:16379/0'
    CELERY_BROKER_URL = 'redis://:npUvCrC3@127.0.0.1:16379/1'
    # 每个worker执行1个任务后销毁重建
    CELERYD_MAX_TASKS_PER_CHILD = 1
    # 防止死锁
    CELERYD_FORCE_EXECV = True

    # 上传文件大小限制 200M
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024

    # 巡检报告工具地址
    REPORT_TOOL_URL = "http://127.0.0.1:8082/api/v1/report"
    # login redis
    LOGIN_REDIS_URL = 'redis://:npUvCrC322@127.0.0.1:16379/2'

    TOKEN_EXP_TIME = 15 * 60

    # URL白名单
    PASS_URL_LIST = [
        "^/auth/",
        "^/static/"
    ]


class DevelopmentConfig(Config):
    """ Development Configuration """
    ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    """ Production Configuration """
    ENV = 'production'
    DEBUG = False


env_conf = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
