# coding=utf-8
from __future__ import unicode_literals

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_docs import ApiDoc
from .config import env_conf

pymysql.install_as_MySQLdb()
base_path = os.path.abspath(os.path.dirname(__file__))
print(base_path)
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static/v1')
    app.config.from_object(env_conf['development'])
    # set_logger()
    db.init_app(app)

    from .views import index, index_404, swaggerui
    # app.add_url_rule('/', 'index', index)
    # app.add_url_rule('/api/docs', 'swaggerui', swaggerui)

    # 使用蓝图（Blueprint）关联程序
    # 关联 api
    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    
    # 关联API文档
    ApiDoc(app)
    return app
