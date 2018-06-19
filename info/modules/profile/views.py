from flask import g
from flask import render_template

from info.utils.commons import login_required
from . import profile_blu


# /user/basic
@profile_blu.route('/basic')
@login_required
def user_basic():
    """
    用户中心-基本信息页面:
    """
    # 从g变量中获取user
    user = g.user

    return render_template('news/user_base_info.html', user=user)


@profile_blu.route('')
@login_required
def get_user_profile():
    """
    用户个人中心页面:
    """
    # 从g变量中获取user
    user = g.user

    return render_template('news/user.html', user=user)
