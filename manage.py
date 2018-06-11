# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    """项目的配置类"""
    DEBUG = True

    # 数据库相关配置
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@172.16.179.139:3306/gz02_info'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 创建Flask应用程序实例
app = Flask(__name__)


# 从配置类中加载配置信息
app.config.from_object(Config)


# 创建SQLAlchemy的对象
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    # 运行开发web服务器
    app.run()
