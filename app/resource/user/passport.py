# 类视图
import random

from flask_restful import Resource
from app import redis_cli
from utils.contants import SMS_CODE_EXPIRE


class SMSCodeResource(Resource):
    """
    发送短信
    """

    def get(self, mobile):
        # 1.产生6位随机数字
        random_smscode = "%06d" % (random.randint(0, 999999))
        # 2.将短信保存在reids中
        # key = "app:code:{}".format(mobile)
        # redis_cli.setex(name=key, time=SMS_CODE_EXPIRE, value=random_smscode)
        # 3.调用第三方平台发送短信
        print("发送短信成功 mobile：{} sms:{}".format(mobile, random_smscode))
        # 返回
        return {"mobile": mobile, "smscode": random_smscode}
