from flask import current_app
from flask import g
from flask import render_template
from flask import session

from info import constants
from info.models import User
from info.utils.commons import login_user_data
from . import news_blu


# get_news_detail.__name__

@news_blu.route('/<int:news_id>')
@login_user_data
def get_news_detail(news_id):
    """
    新闻详情页面:
    """
    # 尝试从session中获取user_id
    # user_id = session.get('user_id')  # 获取不到，返回None
    #
    # user = None
    # if user_id:
    #     # 用户已登录
    #     try:
    #         user = User.query.get(user_id)
    #         user.avatar_url = constants.QINIU_DOMIN_PREFIX + user.avatar_url
    #     except Exception as e:
    #         current_app.logger.error(e)

    # 从g变量中获取user
    user = g.user

    # 使用模板
    return render_template('news/detail.html', user=user)