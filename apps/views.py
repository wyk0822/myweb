# -*- coding: utf-8 -*-

from flask import render_template, make_response


def index():
    return render_template('index.html')

def swaggerui():
    return render_template("swaggerui.html")


def index_404(e):
    response = make_response(render_template('index.html'))
    response.headers['X-404-Redirect'] = True
    response.headers['X-404-Redirect-Info'] = str(e)
    return response
