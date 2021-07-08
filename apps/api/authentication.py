# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import time
import logging
from flask import current_app
from flask import g, jsonify, session, request, make_response
from flask_restful import Resource
from manage import app
from . import auth
from .errors import unauthorized
from .. import db
from apps.utils.exceptions import ValidationError
from ..model.user import User
from ..model.role import Role
from ..model.permission import Permission
from ..utils.verify import verify_password

log = logging.getLogger('webserver.api.auth')


@auth.error_handler
def auth_error():
    return unauthorized('请重新登录!')


class Login(Resource):
    def post(self):
        """登录
            @@@
            ### args
            |  args | nullable | type |  remarks |
            |-------|----------|------|----------|
            | username |  false  | str  | 用户名    |
            | password  |  false | str  | 密码|
            ### request
                {"username": "xxx", "password": "xxx"}
            ### return
                {'username': xxx, 'token': xxx, 'expiration': xxx}
            @@@
        """
        data = request.get_json()
        if not data:
            raise ValidationError('请求参数非法')
        username = data.get('username')
        password = data.get('password')
        if not username:
            raise ValidationError('用户名为空')
        if not password:
            raise ValidationError('密码为空')
        return self._login(username, password)

    def get(self):
        username = request.args.get('username')
        password = request.args.get('password')
        if not username:
            raise ValidationError('用户名为空')
        if not password:
            raise ValidationError('密码为空')
        return self._login(username, password)

    @staticmethod
    def _login(username, password):
        user = User.query.filter_by(username=username).first()
        user.check_permissions(user)
        if user is None:
            return make_response(jsonify({'error': 'unauthorized', 'message': '用户名不存在'}), 403)
        if user.verify_password(password):
            g.current_user = user
            token = user.generate_auth_token(current_app.config['TOKEN_EXP_TIME'])
            # session.permanent = True
            session['username'] = user.username
            session['jwt_token'] = token
            session['jwt_token_expiry'] = int(time()) + current_app.config['TOKEN_EXP_TIME']  # token到这个时间过期
            return make_response(jsonify({
                'username': user.username,
                'token': token,
                'expiration': current_app.config['TOKEN_EXP_TIME']
            }))
        else:
            return make_response(jsonify({'error': 'unauthorized', 'message': '密码错误'}), 403)


class Register(Resource):
    # method_decorators = [auth.login_required]
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username:
            raise ValidationError('用户名不能为空')
        if not verify_password(password):
            raise ValidationError('密码非法')
        user = User(username=username,
                    password_hash=password)
        user.hash_password(password)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise ValidationError("未知数据库错误")
        return make_response(jsonify({'message': 'ok'}))


class Logout(Resource):
    method_decorators = [auth.login_required]

    def get(self):
        # session.permanent = True
        session['jwt_token_expiry'] = 0
        return make_response('', 204)


class ChangePassword(Resource):
    method_decorators = [auth.login_required]

    def post(self):
        data = request.get_json()
        if not data:
            raise ValidationError('请求参数非法')
        username = data.get('username', '')
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        if not username:
            raise ValidationError('用户名为空')
        if not old_password:
            raise ValidationError('原密码为空')
        if not new_password:
            raise ValidationError('新密码为空')
        return self._change_password(username, old_password, new_password)

    def get(self):
        username = request.args.get('username', '')
        old_password = request.args.get('old_password', '')
        new_password = request.args.get('new_password', '')
        if not username:
            raise ValidationError('用户名为空')
        if not old_password:
            raise ValidationError('原密码为空')
        if not new_password:
            raise ValidationError('新密码为空')
        return self._change_password(username, old_password, new_password)

    @staticmethod
    def _change_password(username, old_password, new_password):
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise ValidationError('用户名不存在')
        if not user.verify_password(old_password):
            raise ValidationError('密码校验失败')
        if not verify_password(new_password):
            raise ValidationError('密码校验失败,密码应为8~32位数字和字母组成')

        user.password = new_password
        user.hash_password(new_password)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise ValidationError("未知数据库错误")
        # session.permanent = True
        session['jwt_token_expiry'] = 0
        return make_response(jsonify({"message": "修改成功，请重新登录"}))

    @staticmethod
    def _reset_password(username, new_password):

        user = User.query.filter_by(username=username).first()
        if user is None:
            return False, '用户名不存在'
        if not verify_password(new_password):
            return False, '密码校验失败,密码应为8~32位数字和字母组成'
        user.password = new_password
        user.hash_password(new_password.encode())
        db.session.add(user)
        status = True
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return False, "未知数据库错误"
        return status, '修改密码成功!'


class TokenPing(Resource):
    method_decorators = [auth.login_required]

    def get(self):
        user = auth.current_user()
        token = user.generate_auth_token(app.config['TOKEN_EXP_TIME'])
        session['jwt_token'] = token
        session['jwt_token_expiry'] = int(time()) + current_app.config['TOKEN_EXP_TIME']
        return make_response(jsonify({"message": "pong", "token": token}))
