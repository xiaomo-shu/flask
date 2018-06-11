# coding=utf-8
import redis
from flask import session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from config import Config


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

# pip install flask-session
# session存储设置
Session(app)


# 创建Manager对象
manager = Manager(app)
Migrate(app, db)
# 添加命令行数据库管理命令`db`
manager.add_command('db', MigrateCommand)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis
    # redis_store.set('name', 'itcast')

    # 测试session
    session['name'] = 'itheima'
    return 'index'

if __name__ == '__main__':
    # 运行开发web服务器
    # app.run()
    manager.run()