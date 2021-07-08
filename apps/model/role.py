# -*- coding: UTF-8 -*-
# @author: qatest01
# @file: role.py
# @time: 2021/05/27
# @Project: testPlatform
from apps import db

# 使用db.tables创建第三张关联表，不需要对应的实体类
role_permission = db.Table(
    # 指定关联表的表名
    'role_permission',
    # 指定关联表的主键
    db.Column('id', db.Integer, primary_key=True),
    # 指定外键，关联Student表的主键
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    # 指定外键，关联course表的主键
    db.Column('Permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=True)
    # 与生成表结构无关，仅用于查询方便
    permission = db.relationship('Permission', secondary='role_permission',lazy='dynamic',
                                 backref=db.backref('role', lazy='dynamic'))

    def __repr__(self):
        return self.name

    def has_permission(self):
        pass
