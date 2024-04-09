import os, sys
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from redis import StrictRedis
from app.settings.config import config_dict
from common.utils import contants

# 将common文件添加到python搜索路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH + '/common')
# print(BASE_PATH)


####################添加数据库###################
# 方法1：db=SQLAlchemy(app)

# 方法2：
# 由于app被封装采用延后加载app数据库配置信息方法初始化数据库对象
# 定义成全局变量，方便别的模块调用

db = SQLAlchemy()

# redis客户端同样需要暴露成全局变量，方便模块调用

redis_cli = None  # type: StrictRedis


def create_flask_app(type):
    '''
    内配调用的生产app的方法
    :param type:根据配置文件中传入的的配置信息生产app
    :return:对应配置的app对象
    '''

    # 1.创建app对象
    app = Flask(__name__)
    # 2.读取配置类的配置信息
    app.config.from_object(config_dict[type])
    # 3.读取环境变量中的配置信息
    app.config.from_envvar(contants.EXTRA_ENV_CONFIG, silent=True)
    return app


def create_app(type):
    '''
    外界调用的生产app的工厂方法
    :param type: 配置的类型
    :return: app
    '''
    # 1.调用内容方法生产app
    app = create_flask_app(type)
    # 2.注册拓展初始化组件
    register_extentions(app)
    # 3.注册蓝图初始化组件

    return app


def register_extentions(app: Flask):  # 声明app形参传入的是什么
    '''注册拓展初始化组件'''

    # 1.延后加载app，进行mysql数据库对象初始化
    db.init_app(app)

    # 2.延后加载app中redis哭护短配置信息，然后创建redis客户端对象

    global redis_cli
    #decode_responses=True将返回的bytes类型转为str
    redis_cli = StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], decode_responses=True)
    pass
