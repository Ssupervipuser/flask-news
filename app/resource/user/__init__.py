# 用户模块
from flask import Blueprint
from flask_restful import Api
from utils.contants import URL_PREFIX
from app.resource.user.passport import SMSCodeResource, LoginRegisterResource
from utils.output import output_json

# 1.创建蓝图对象
user_bp = Blueprint('user_bp', __name__, url_prefix=URL_PREFIX)
# 2.包装成restful风格对象
# 参数1：app对象或者蓝图对象
user_api = Api(user_bp)
# 3.自定义类视图

# 4.给类视图添加路由信息
user_api.add_resource(SMSCodeResource, '/sms/code/<mob:mobile>')
user_api.add_resource(LoginRegisterResource, '/authorization')

# 5.在app中注册蓝图对象

# 6.自定义json返回格式

'''
{
    "message":"OK",
    "data":"{
            shujv
            }"
}
'''
# 使用装饰器主动装饰视图函数
user_api.representation(mediatype="application/json")(output_json)
