# -*- coding: utf-8 -*-
from jinja2 import TemplateError


class AppRenderValueError(ValueError):
    pass


class AppRenderIOError(IOError):
    pass


class AppRenderKeyError(KeyError):
    pass


class AppRenderTypeError(TypeError):
    pass


class AppRenderTemplateError(TemplateError):
    pass


class ValidationError(ValueError):
    pass


class DuplicateError(ValueError):
    pass