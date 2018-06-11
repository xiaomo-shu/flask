# coding=utf-8
from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from info import create_app, db

# 需求: 只修改manage.py文件中的相应代码，
# 获取不同配置环境下的app对象
app = create_app('development')

# 创建Manager对象
manager = Manager(app)
Migrate(app, db)
# 添加命令行数据库管理命令`db`
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # 运行开发web服务器
    app.run()
    # manager.run()
