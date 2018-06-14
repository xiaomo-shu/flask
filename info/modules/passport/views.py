from . import passport_blu

from flask import make_response

from info.utils.captcha.captcha import captcha


@passport_blu.route('/image_code')
def get_image_code():
    """
    产生图片验证码:
    """

    # 产生图片验证码
    # 图片名称 验证码文本 验证码图片内容
    name, text, content = captcha.generate_captcha()

    # 返回验证码图片
    response = make_response(content)
    # 设置响应的数据类型
    response.headers['Content-Type'] = 'image/jpg'
    return response
