# coding=utf-8
from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from info import create_app, db, models

# 需求: 只修改manage.py文件中的相应代码，
# 获取不同配置环境下的app对象
from info.models import User

app = create_app('development')

# 创建Manager对象
manager = Manager(app)
Migrate(app, db)
# 添加命令行数据库管理命令`db`
manager.add_command('db', MigrateCommand)


@manager.option('-n', '-name', dest='name')
@manager.option('-p', '-password', dest='password')
def createsuperuser(name, password):
    """创建管理员用户"""
    if not all([name, password]):
        print('参数不足')
        return

    user = User()
    user.mobile = name
    user.nick_name = name
    user.password = password
    user.is_admin = True

    try:
        db.session.add(user)
        db.session.commit()
        print("创建成功")
    except Exception as e:
        print(e)
        db.session.rollback()


if __name__ == '__main__':
    # 运行开发web服务器
    # app.run()
    manager.run()
