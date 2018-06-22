from flask import current_app
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from info.models import User
from info.utils.commons import admin_login_required
from . import admin_blu


# /admin/index
@admin_blu.route('/index')
@admin_login_required
def index():
    """
    后台管理首页:
    """
    # 获取当前登录用户user
    user = g.user

    return render_template('admin/index.html', user=user)


# /admin/login
@admin_blu.route('/login', methods=['GET', 'POST'])
def login():
    """
    后台管理员登录页面:
    """
    if request.method == 'GET':
        # 显示页面
        user_id = session.get('user_id')
        is_admin = session.get('is_admin')

        if user_id and is_admin:
            # 管理员已登录
            return redirect(url_for('admin.index'))

        return render_template('admin/login.html')
    else:
        # 进行登录处理
        # 1. 接收参数并进行参数校验
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            flash('参数不完整')
            # 重定向的请求方式是GET
            return redirect(url_for('admin.login'))

        # 2. 根据`username`去查询管理员用户的信息
        try:
            user = User.query.filter(User.nick_name == username,
                                     User.is_admin == True).first()
        except Exception as e:
            current_app.logger.error(e)
            flash('服务器错误')
            return redirect(url_for('admin.login'))

        if not user:
            flash('用户不存在')
            return redirect(url_for('admin.login'))

        # 3. 校验用户的登录密码是否正确
        if not user.check_passowrd(password):
            flash('密码错误')
            return redirect(url_for('admin.login'))

        # 4. 在session中记住用户的登录状态
        session['user_id'] = user.id
        session['nick_name'] = user.nick_name
        session['mobile'] = user.mobile
        session['is_admin'] = True

        # 5. 登录成功，跳转到后台管理的首页
        # return '后台管理首页'
        return redirect(url_for('admin.index'))