# -*- coding: UTF-8 -*-
# @author: qatest01
# @file: permission.py
# @time: 2021/05/27
# @Project: testPlatform
from apps import db


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    url = db.Column(db.String(128))
    # menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"))
    #
    # menu = db.relationship("Menus", backref='permission')

    def __repr__(self):
        return self.name
