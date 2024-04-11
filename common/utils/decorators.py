# 装饰器模块
import functools
from flask import g

"""
业务逻辑
user id None==>未登录
user_id=6同时is_refresh=True==>刷新token==>访问刷新接口
user_id=6同时is_refresh=Flase==>,登录token==>进入视图函数
"""


# 强制登录装饰器
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = g.user_id
        # 装饰器添加的额外功能
        if user_id is None:
            # 未登录--401权限验证失败【未携带token，token过期，错误token】
            return {'message': "invalid token"}, 401
        elif user_id and g.is_refresh is True:
            #403 刷新token不能做用户权限认证
            return {'message': " can't use refresh_token to loin"}, 403
        else:
            #登录token 允许访问视图函数
            return view_func(*args,**kwargs)


            # 原有函数功能

    return wrapper()
