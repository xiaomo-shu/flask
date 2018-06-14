from flask import abort, jsonify
from flask import current_app
from flask import request

from info import constants
from info.utils.response_code import RET
from . import passport_blu

from flask import make_response

from info import redis_store
from info.utils.captcha.captcha import captcha


@passport_blu.route('/image_code')
def get_image_code():
    """
    产生图片验证码:
    1. 接收参数(图片验证码标识image_code_id)并且进行参数校验
    2. 产生图片验证码
    3. 在redis中保存验证码文本，以`图片验证码标识`为key，以验证码文本为value
    4. 返回验证码图片
    """
    # 1. 接收参数(图片验证码标识image_code_id)并且进行参数校验
    image_code_id = request.args.get('image_code_id')

    if not image_code_id:
        # abort(400)
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 2. 产生图片验证码
    # 图片名称 验证码文本 验证码图片内容
    name, text, content = captcha.generate_captcha()

    # 3. 在redis中保存验证码文本，以`图片验证码标识`为key，以验证码文本为value
    try:
        redis_store.set('image_code:%s' % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存图片验证码失败')

    # 4. 返回验证码图片
    response = make_response(content)
    # 设置响应的数据类型
    response.headers['Content-Type'] = 'image/jpg'
    return response
