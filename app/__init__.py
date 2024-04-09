import os, sys

from flask import Flask

from app.settings.config import config_dict
from common.utils import contants

# 将common文件添加到python搜索路径

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH + '/common')
# print(BASE_PATH)


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
    app=create_flask_app(type)
    # 2.注册拓展初始化组件

    # 3.注册蓝图初始化组件

    return app
