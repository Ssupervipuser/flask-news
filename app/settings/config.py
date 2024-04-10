# 系统配置信息
from flask_sqlalchemy import SQLAlchemy


class DefalutConfig():
    '''醒目默认配置信息'''
    # session加密字符串
    SECRET_KEY = 'flask_news'

    # flask-restful防止返回中文为ascii编码格式
    RESTFUL_JSON = {'ensure_ascii': False}

    # mysql连接配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@192.168.10.131:3306/flasknews'
    # 输出执行的sql语言
    SQLALCHEMY_ECHO = True

    # redis连接配置
    REDIS_HOST = '1'
    # 需要连接主库
    REDIS_PORT = 6381


class DevelopmentConfig(DefalutConfig):
    '''开发环境配置信息'''
    DEBUG = True


class ProductionConfig(DefalutConfig):
    '''生产环境配置信息'''

    DEBUG = True

    # mysql连接配置

    # redis连接配置


# 外界条用暴露字典接口
config_dict = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
}
