from flask import current_app
from flask import render_template
from flask import session

from info import constants
from info.models import User
from . import news_blu


@news_blu.route('/<int:news_id>')
def get_news_detail(news_id):
    """
    新闻详情页面:
    """
    # 尝试从session中获取user_id
    user_id = session.get('user_id')  # 获取不到，返回None

    user = None
    if user_id:
        # 用户已登录
        try:
            user = User.query.get(user_id)
            user.avatar_url = constants.QINIU_DOMIN_PREFIX + user.avatar_url
        except Exception as e:
            current_app.logger.error(e)

    # 使用模板
    return render_template('news/detail.html', user=user)