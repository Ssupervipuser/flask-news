# 中间件

from flask import g, request, current_app
from utils.jwt_util import verify_jwt


def get_userinfo():
    """
    每一次请求之前调用该方法统一提取token中的用户信息
    :return:
    """
    # 要求前端在请求头中携带token值{"Authorization":token}

    # 1.提取前端写到的token值
    token = request.headers.get("Authorization")
    secret = current_app.config['JWT_SECRET']

    g.user_id = None
    g.is_refresh = False
    '''
    #未登录
    g.user_id=None
    g.is_refresh=False
    #登录token
    g.user_id=id
    g.is_refresh=False
    #刷新token
    g.user_id=None
    g.is_refresh=False
    '''
    # 2.校验token，提取载荷信息
    if token:
        try:
            payload = verify_jwt(token, secret=secret)
        except Exception as e:
            payload = None
        # 3.从载荷字典中提取用户信息，保存到g对象【能在g钩子和视图之间传递值】
        if payload:
            g.user_id = payload.get('user_id')
            g.is_refresh = payload.get('is_refresh', False)
