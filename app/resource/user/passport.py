# 类视图
import random
from datetime import datetime, timedelta
from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import redis_cli, db
from model.user import User
from utils.contants import SMS_CODE_EXPIRE
from utils.parser import mobile as type_mobile, regex
from utils.jwt_util import generate_jwt


class SMSCodeResource(Resource):
    """
    发送短信
    """

    def get(self, mobile):
        # 1.产生6位随机数字
        random_smscode = "%06d" % (random.randint(0, 999999))
        # 2.将短信保存在reids中
        key = "app:code:{}".format(mobile)
        redis_cli.setex(name=key, time=SMS_CODE_EXPIRE, value=random_smscode)
        # 3.调用第三方平台发送短信
        print("发送短信成功 mobile：{} sms:{}".format(mobile, random_smscode))
        # 返回
        return {"mobile": mobile, "smscode": random_smscode}
        # return {"mobile": mobile, "smscode": 123456}


class LoginRegisterResource(Resource):

    def _generator_token(self, user_id):
        """
        生成2htoken
        14h refresh_token【待2h登录token失效之后，使用token刷新一个新的2h有效token】
        :param user_id:当前登录用户id
        :return: token&refresh_token
        """
        # 1.生成2htoken
        # payload
        login_payload = {
            'user_id': user_id,
            'is_refresh': False
        }
        # 2h过期时长
        expire_2h = datetime.utcnow() + timedelta(hours=current_app.config['JWT_LOGIN_EXPIRE'])
        # 生成token
        token = generate_jwt(payload=login_payload, expiry=expire_2h, secret=current_app.config['JWT_SECRET'])

        # 2. 14h token
        # payload
        refresh_payload = {
            'user_id': user_id,
            'is_refresh': False
        }
        # 14h过期时长
        expire_14h = datetime.utcnow() + timedelta(hours=current_app.config['JWT_REFRESH_EXPIRE'])
        # 生成token
        refresh_token = generate_jwt(payload=refresh_payload, expiry=expire_14h, secret=current_app.config['JWT_SECRET'])

        return token, refresh_token

    """
    # 1.获取参数
    #     1.手机号码
    #     2.用户填写的短信验证码 要求前端从json字符串中发送请求参数
    # 2.参数校验
    #
    # 3.逻辑处理【增删改查】
    #     1.根据手机号码凭借短信验证码的key，查询真实的短信验证码值
    #     2.删除短信验证码【防止多次使用同一个短信验证码验证多次】
    #     3.判断取出的真实短信验证码是否有值，用户填写与真实验证码是否一致
    #     4.条件满足：根据手机号码去数据库查询用户是否存在
    #     5.用户存在：登录--修改最有一次登陆时间
    #     6.用户不存在新建用户添加到数据库
    #     7.提交到数据库
    #
    # 4.return
    #     1.返回2小时有效的登录token（某些视图需要验证的token），返回14天有效的刷新token（过期需要登录）
    """

    def post(self):
        # 1.获取参数

        # 2.参数校验
        parser = RequestParser()
        parser.add_argument('mobile', required=True, location='json', type=type_mobile)
        parser.add_argument('code', required=True, location='json', type=regex(r'\d{6}'))
        ret = parser.parse_args()
        #     1.手机号码
        mobile = ret['mobile']
        #     2.用户填写的短信验证码 要求前端从json字符串中发送请求参数
        code = ret['code']

        # 3.逻辑处理【增删改查】
        #     1.根据手机号码凭借短信验证码的key，查询真实的短信验证码值
        key = 'app:code:{}'.format(mobile)
        real_smscode = redis_cli.get(key)

        #     2.删除短信验证码【防止多次使用同一个短信验证码验证多次】
        # redis_cli.delete(key)

        #     3.判断取出的真实短信验证码是否有值，用户填写与真实验证码是否一致
        # tip:redis取出的值是b类型，前面已经转换过
        if real_smscode is None or code != real_smscode:
            return {'message': 'invalid smscode'}, 400
        #     4.条件满足：根据手机号码去数据库查询用户是否存在
        user = User.query.options(load_only(User.id)).filter(User.mobile == mobile).first()
        #     6.用户不存在新建用户添加到数据库
        if user is None:
            user = User(name=mobile, mobile=mobile, last_login=datetime.now())
            db.session.add(user)
        #     5.用户存在：登录--修改最有一次登陆时间
        else:
            user.last_login = datetime.now()

        #     7.提交到数据库
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': e}, 507
        # 4.return
        #  todo:   1.返回2小时有效的登录token（某些视图需要验证的token），返回14天有效的刷新token（过期需要登录）
        token, refresh_token = self._generator_token(user.id)
        return {"token": token, "refresh_token": refresh_token}

    def put(self):

        #todo:刷新token逻辑实现
        pass