# -*- coding: UTF-8 -*-
# @author: qatest01
# @file: test_rbac.py
# @time: 2021/05/28
# @Project: testPlatform

from flask_restful import Resource
from flask import request, make_response, jsonify

from apps import db
from apps.utils.exceptions import ValidationError
from ..model.user import User
from ..model.role import Role
from ..model.permission import Permission

class Rbac_test(Resource):
    def post(self):
        pass

    def get(self, id):
        print(id, type(id))
        obj = User.query.filter_by(id=id).first()
        print(obj)
        return "ok"


class Rbac_Role(Resource):
    def post(self):
        name = request.form.get("name")
        if name is None:
            raise ValidationError('角色名为空')
        else:
            role = Role(name=name)
        db.session.add(role)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise ValidationError("未知数据库错误")
        return make_response(jsonify({'message': 'ok'}))

    def get(self):

        self._user()
        return make_response(jsonify({'message': 'ok', 'pres': "22"}))
    def _user(self):
        name = request.args.get("name")
        roleid = request.args.get("roleid")
        print(name, roleid)
        user = User.query.filter_by(id=name).first()
        print(user)

        role = Role.query.filter_by(id=roleid).first()
        print(role)

        user.role.append(role)

        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise ValidationError("未知数据库错误")
        roles = user.role.all()
        print(roles)

    def _role(self):
        name = request.args.get("name")
        preid = request.args.get("per")
        print(name, preid)
        role = Role.query.filter_by(id=name).first()
        print(role)

        pre = Permission.query.filter_by(id=preid).first()
        print(pre)

        role.permission.append(pre)

        db.session.add(role)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise ValidationError("未知数据库错误")
        pres = role.permission.all()
        print(pres)
        return make_response(jsonify({'message': 'ok', 'pres': "22"}))







class Rbac_Permission(Resource):
    def post(self):
        name = request.form.get("name")
        url = request.form.get("url")
        permission = Permission(name=name, url=url)
        db.session.add(permission)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise ValidationError("未知数据库错误")
        return make_response(jsonify({'message': 'ok'}))

