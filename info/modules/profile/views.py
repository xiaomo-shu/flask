from flask import current_app
from flask import g, jsonify
from flask import render_template
from flask import request
from flask import session

from info import db
from info.utils.commons import login_required
from info.utils.response_code import RET
from . import profile_blu


# /user/avatar
@profile_blu.route('/avatar')
@login_required
def user_avatar():
    """
    用户中心-个人头像页面:
    """
    # 从g变量中获取user
    user = g.user

    return render_template('news/user_pic_info.html', user=user)


# /user/basic
@profile_blu.route('/basic', methods=['GET', 'POST'])
@login_required
def user_basic():
    """
    用户中心-基本信息页面:
    """
    # 从g变量中获取user
    user = g.user
    
    if request.method == 'GET':
        return render_template('news/user_base_info.html', user=user)
    else:
        # 保存修改用户的信息
        # 1. 接收参数并进行参数校验
        req_dict = request.json

        if not req_dict:
            return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

        signature = req_dict.get('signature')
        nick_name = req_dict.get('nick_name')
        gender = req_dict.get('gender')

        if not all([signature, nick_name, gender]):
            return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

        if gender not in ('MAN', 'WOMAN'):
            return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

        # 2. 设置用户的个人信息
        user.signature = signature
        user.nick_name = nick_name
        user.gender = gender
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='保存用户信息失败')

        # 设置session中的nick_name
        session['nick_name'] = nick_name
        
        # 3. 返回应答，设置个人信息成功
        return jsonify(errno=RET.OK, errmsg='设置个人信息成功')
            

@profile_blu.route('')
@login_required
def get_user_profile():
    """
    用户个人中心页面:
    """
    # 从g变量中获取user
    user = g.user

    return render_template('news/user.html', user=user)
