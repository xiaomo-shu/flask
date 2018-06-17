from flask import render_template

from . import news_blu


@news_blu.route('/<int:news_id>')
def get_news_detail(news_id):
    """
    新闻详情页面:
    """
    # 使用模板
    return render_template('news/detail.html')