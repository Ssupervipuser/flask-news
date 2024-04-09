class DefalutConfig():
    '''醒目默认配置信息'''
    #session加密字符串
    SECRET_KEY='flask_news'


class DevelopmentConfig(DefalutConfig):
    '''开发环境配置信息'''
    DEBUG=True

    #mysql连接配置

    #redis连接配置


class ProductionConfig(DefalutConfig):
    '''生产环境配置信息'''

    DEBUG=True

    # mysql连接配置

    # redis连接配置


#外界条用暴露字典接口
config_dict={
    'dev':DevelopmentConfig,
    'pro':ProductionConfig,
}
