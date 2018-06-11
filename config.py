import redis


class Config(object):
    """项目的配置类"""
    DEBUG = True

    # 设置SECRET_KEY
    SECRET_KEY = 'NmwKKxmKOSZrjTGVOI04o9RBj0/t3hcYDHFQ7TDD7zr803t+qMuKciveDNrot1Qd'

    # 数据库相关配置
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@172.16.179.139:3306/gz02_info'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库的相关配置
    REDIS_HOST = '172.16.179.139'
    REDIS_PORT = 6379

    # session存储的相关配置
    # 设置session存储到redis中
    SESSION_TYPE = 'redis'
    # redis链接对象(给flask-session扩展使用的)
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启返回给浏览器cookie `session`值的加密
    SESSION_USE_SIGNER = True
    # 设置session过期时间
    PERMANENT_SESSION_LIFETIME = 24*3600*2
