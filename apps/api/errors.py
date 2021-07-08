# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlite3 import IntegrityError

from flask import jsonify

from . import api_bp as api

from ..utils.exceptions import (AppRenderValueError,
                                AppRenderIOError,
                                AppRenderKeyError,
                                AppRenderTypeError,
                                AppRenderTemplateError,
                                ValidationError,
                                DuplicateError
                                )


def not_found(message):
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def conflict(message):
    response = jsonify({'error': 'conflict', 'message': message})
    response.status_code = 409
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(AppRenderValueError)
def app_render_value_error(e):
    response = jsonify({'error': 'value error', 'message': e.args[0]})
    response.status_code = 400
    return response


@api.errorhandler(AppRenderIOError)
def app_render_io_error(e):
    response = jsonify({'error': 'io error', 'message': e.args[0]})
    response.status_code = 400
    return response


@api.errorhandler(AppRenderKeyError)
def app_render_key_error(e):
    response = jsonify({'error': 'key error', 'message': e.args[0]})
    response.status_code = 400
    return response


@api.errorhandler(AppRenderTypeError)
def app_render_type_error(e):
    response = jsonify({'error': 'type error', 'message': e.args[0]})
    response.status_code = 400
    return response


@api.errorhandler(AppRenderTemplateError)
def app_render_template_error(e):
    response = jsonify({'error': 'template error', 'message': e.args[0]})
    response.status_code = 400
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@api.errorhandler(DuplicateError)
def duplicate_error(e):
    return conflict(e.args[0])


@api.errorhandler(IntegrityError)
def integrity_error(e):
    return bad_request(e.args[0])


@api.errorhandler(404)
def not_found_404(e):
    return not_found('访问的资源不存在')


@api.after_request
def header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Headers'] = 'authorization,content-type,x-requested-with'
    response.headers['Access-Control-Max-Age'] = 2592000
    response.headers['Access-Control-Allow-Methods'] = "GET,HEAD,PUT,POST,DELETE"
    return response
