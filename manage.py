# coding=utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from info import app, db

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
    # session['name'] = 'itheima'
    return 'index'

if __name__ == '__main__':
    # 运行开发web服务器
    # app.run()
    manager.run()