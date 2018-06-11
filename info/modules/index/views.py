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

    return 'index'
