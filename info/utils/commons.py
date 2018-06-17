# 此文件中定义我们自己封装一些代码
import functools
from flask import current_app
from flask import g
from flask import session

from info import constants
from info.models import User


def do_rank_class(index):
    """获取点击排行新闻对应class"""
    if index < 0 or index >= 3:
        return ''

    rank_class_li = ['first', 'second', 'third']

    return rank_class_li[index]


def login_user_data(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 尝试从session中获取user_id
        user_id = session.get('user_id')  # 获取不到，返回None

        user = None
        if user_id:
            # 用户已登录
            try:
                user = User.query.get(user_id)
                user.avatar_url = constants.QINIU_DOMIN_PREFIX + user.avatar_url if user.avatar_url else ''

                # if user.avatar_url:
                #     constants.QINIU_DOMIN_PREFIX + user.avatar_url
                # else:
                #     ''
            except Exception as e:
                current_app.logger.error(e)

        # 使用g变量临时保存user信息
        # g变量中保存的数据可以在请求开始到请求结束过程中的使用
        g.user = user

        return view_func(*args, **kwargs)

    return wrapper
