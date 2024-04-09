#项目启动文件
from flask import jsonify

from app import create_app

#调用工厂方法创建app对象
app=create_app('dev')

@app.route('/')
def index():
    #返回所有路由信息
    #字典推导式
    route_dic={rule.rule:rule.endpoint for rule in app.url_map.iter_rules()}
    return jsonify(route_dic)