from flask import abort
from flask import current_app
from flask import g
from flask import render_template
from flask import session

from info import constants, db
from info.models import User, News
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

    # 根据`news_id`获取新闻详情信息
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)

    if not news:
        abort(404)

    # 新闻`点击量`+1
    news.clicks += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

    # 获取`点击排行`的新闻信息
    rank_news_li = []
    try:
        rank_news_li = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)

    # 使用模板
    return render_template('news/detail.html',
                           user=user,
                           news=news,
                           rank_news_li=rank_news_li)