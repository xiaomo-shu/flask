from flask import current_app
from flask import render_template
from flask import session

from info import constants
from info.models import User, News
from . import index_blu
from info import redis_store


# 2. 使用蓝图对象注册路由
@index_blu.route('/', methods=['GET', 'POST'])
def index():
    # 尝试从session中获取user_id
    user_id = session.get('user_id') # 获取不到，返回None

    user = None
    if user_id:
        # 用户已登录
        try:
            user = User.query.get(user_id)
            user.avatar_url = constants.QINIU_DOMIN_PREFIX + user.avatar_url
        except Exception as e:
            current_app.logger.error(e)

    # 获取`点击排行`的新闻信息
    rank_news_li = []
    try:
        rank_news_li = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)

    # 使用模板
    return render_template('news/index.html',
                           user=user,
                           rank_news_li=rank_news_li)


# 当浏览器访问一个网站时，会默认访问网站下的路径/favicon.ico
# 目的就是获取网站图标文件
@index_blu.route('/favicon.ico')
def get_web_ico():
    """获取网站的图标"""
    # current_app.send_static_file: 获取静态目录下文件的内容
    # current_app.send_static_file('news/html/user.html')
    return current_app.send_static_file('news/favicon.ico')
