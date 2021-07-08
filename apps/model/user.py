# -*- coding: utf-8 -*-

from datetime import datetime
from time import time

from flask import current_app
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer

from apps.api import auth
from apps import db
user_role = db.Table(
    # 指定关联表的表名
    'user_role',
    # 指定关联表的主键
    db.Column('id', db.Integer, primary_key=True),
    # 指定外键，关联user表的主键
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    # 指定外键，关联role表的主键
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)




class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    role = db.relationship('Role', secondary='user_role',lazy='dynamic', backref=db.backref('user', lazy='dynamic'))


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')
    #
    # @password.setter
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)
    #
    # def generate_auth_token(self):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     return s.dumps({'id': self.id, 'timestamp': str(time())}).decode('utf-8')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return None
    #     user = User.query.get(data['id'])
    #     return user

    @auth.verify_token
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            print(data)
            # print(jwt.decode(token, "223231asdasd", algorithms=['HS256']))
            # print("22222")
        except:
            return
        return User.query.get(data['id'])

    # 获取用户所属角色与用户个人私有权限，判断该用户是否用于要访问的功能的权限．
    def check_permissions(self, user):
        print(current_app.config['PASS_URL_LIST'])
        roles = user.role.all()
        for role in roles:
            print(role.permission.all())