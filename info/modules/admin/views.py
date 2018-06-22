from datetime import datetime, timedelta

from flask import abort
from flask import current_app, jsonify
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from info import constants
from info.models import User, News
from info.utils.commons import admin_login_required
from info.utils.response_code import RET
from . import admin_blu

from info import db
from sqlalchemy import extract


@admin_blu.route('/news/review')
@admin_login_required
def news_review():
    """
    后台管理-新闻审核列表页面:
    """
    # 1. 获取参数并进行校验
    page = request.args.get('p', 1)
    key = request.args.get('key')

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    # 2. 获取所有新闻的信息并进行分页
    filters = []
    if key:
        filters.append(News.title.contains(key))

    try:
        pagination = News.query.filter(*filters). \
            order_by(News.create_time.desc()). \
            paginate(page, constants.ADMIN_NEWS_PAGE_MAX_COUNT, False)

        news_li = pagination.items
        total_page = pagination.pages
        current_page = pagination.page
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    # 3. 使用模板
    return render_template('admin/news_review.html',
                           news_li=news_li,
                           total_page=total_page,
                           current_page=current_page)


@admin_blu.route('/user/list')
@admin_login_required
def user_list():
    """
    后台管理-用户列表信息页面:
    """
    # 1. 获取参数并进行校验
    page = request.args.get('p', 1)

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    # 2. 获取所有普通用户信息并进行分页
    try:
        pagination = User.query.order_by(User.create_time.desc()). \
            paginate(page, constants.ADMIN_USER_PAGE_MAX_COUNT, False)
        users = pagination.items
        total_page = pagination.pages
        current_page = pagination.page
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    # 3. 使用模板文件
    return render_template('admin/user_list.html',
                           users=users,
                           total_page=total_page,
                           current_page=current_page)


# /admin/user/count
@admin_blu.route('/user/count')
@admin_login_required
def user_count():
    """
    后台管理-用户统计页面:
    """
    # 统计网站用户的总数
    total_count = User.query.count()

    # 统计当月用户的新增数量
    now_date = datetime.now()  # datetime
    year = now_date.year
    month = now_date.month

    month_count = db.session.query(User).filter(extract('year', User.create_time) == year,
                                                extract('month', User.create_time) == month).count()

    # 统计当天用户的新增数量
    day = now_date.day
    day_count = db.session.query(User).filter(extract('year', User.create_time) == year,
                                              extract('month', User.create_time) == month,
                                              extract('day', User.create_time) == day).count()

    # 统计最近30天每天用户新增数量
    counts_li = []
    date_li = []
    begin_date = now_date - timedelta(days=29)

    for i in range(0, 30):
        # 计算当前日期
        cur_date = begin_date + timedelta(days=i)

        # 获取当前日期的年月日
        year = cur_date.year
        month = cur_date.month
        day = cur_date.day

        # 计算出当天新增用户数量
        count = db.session.query(User).filter(extract('year', User.create_time) == year,
                                              extract('month', User.create_time) == month,
                                              extract('day', User.create_time) == day).count()

        # 把当天新增用户数量保存在counts_li列表中
        counts_li.append(count)

        # 保存当前日期
        date_str = cur_date.strftime('%Y-%m-%d')
        date_li.append(date_str)

    return render_template('admin/user_count.html',
                           total_count=total_count,
                           month_count=month_count,
                           day_count=day_count,
                           counts_li=counts_li,
                           date_li=date_li)


# /admin/logout
@admin_blu.route('/logout', methods=['POST'])
def logout():
    """
    管理员退出登录:
    1. 清除session对应的登录信息
    2. 返回应答，退出成功
    """
    # 1. 清除session对应的登录信息
    session.pop('user_id')
    session.pop('mobile')
    session.pop('nick_name')
    session.pop('is_admin')

    # 2. 返回应答，退出成功
    return jsonify(errno=RET.OK, errmsg='退出成功')


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
