from flask import Blueprint
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp, default_mediatype='application/json')

# Authorization: Bearer "JWT..."
auth = HTTPTokenAuth("JWT")

from . import (
    authentication,
    test_rbac
)


# 平台登录
login = authentication.Login.as_view('login')
api_bp.add_url_rule('/auth/login/', view_func=login)

# 退出登录
logout = authentication.Logout.as_view('logout')
api_bp.add_url_rule('/auth/logout/', view_func=logout)

# 重设密码
cpassword = authentication.ChangePassword.as_view('cpassword')
api_bp.add_url_rule('/auth/change-password/', view_func=cpassword)

# token续期
tping = authentication.TokenPing.as_view('tping')
api_bp.add_url_rule('/auth/ping/', view_func=tping)

# 注册用户
register = authentication.Register.as_view('register')
api_bp.add_url_rule('/auth/register/', view_func=register)



rbac = test_rbac.Rbac_test.as_view("rbac")
api_bp.add_url_rule('/rbac/<int:id>/', view_func=rbac)

role = test_rbac.Rbac_Role.as_view("role")
api_bp.add_url_rule('/rbac/role/', view_func=role)

permission = test_rbac.Rbac_Permission.as_view("permission")
api_bp.add_url_rule('/rbac/permission/', view_func=permission)
