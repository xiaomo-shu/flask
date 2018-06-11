# coding=utf-8
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


class Config(object):
    """项目的配置类"""
    DEBUG = True

    # 设置SECRET_KEY
    SECRET_KEY = 'NmwKKxmKOSZrjTGVOI04o9RBj0/t3hcYDHFQ7TDD7zr803t+qMuKciveDNrot1Qd'

    # 数据库相关配置
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@172.16.179.139:3306/gz02_info'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库的相关配置
    REDIS_HOST = '172.16.179.139'
    REDIS_PORT = 6379


# 创建Flask应用程序实例
app = Flask(__name__)


# 从配置类中加载配置信息
app.config.from_object(Config)


# 创建SQLAlchemy的对象
db = SQLAlchemy(app)

# 创建redis链接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 为Flask项目开启CSRF保护
# CSRFProtect只做保护验证工作，所有我们之后需要自己完成2步:
# 1. 生成crsf_token
# 2. 告诉浏览器生成的csrf_token
CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis
    # redis_store.set('name', 'itcast')
    return 'index'

if __name__ == '__main__':
    # 运行开发web服务器
    app.run()
