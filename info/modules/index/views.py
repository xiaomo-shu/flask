from flask import current_app
from flask import render_template

from . import index_blu
from info import redis_store


# 2. 使用蓝图对象注册路由
@index_blu.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis
    redis_store.set('name', 'itcast')

    # 测试session
    # session['name'] = 'itheima'

    # 演示日志输出
    # import logging
    # logging.fatal('Fatal Message')
    # logging.error('Error Message')
    # logging.warning('Warning Message')
    # logging.info('Info Message')
    # logging.debug('Debug Message')

    # 演示flask项目中输出日志
    # current_app.logger.fatal('Fatal Message')
    # current_app.logger.error('Error Message')
    # current_app.logger.warning('Warning Message')
    # current_app.logger.info('Info Message')
    # current_app.logger.debug('Debug Message')

    # TODO 要做的工作

    # return 'index'

    return render_template('news/index.html')


# 当浏览器访问一个网站时，会默认访问网站下的路径/favicon.ico
# 目的就是获取网站图标文件
@index_blu.route('/favicon.ico')
def get_web_ico():
    """获取网站的图标"""
    # current_app.send_static_file: 获取静态目录下文件的内容
    # current_app.send_static_file('news/html/user.html')
    return current_app.send_static_file('news/favicon.ico')
