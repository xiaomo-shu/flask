# coding=utf-8
from flask import Flask

# 创建Flask应用程序实例
app = Flask(__name__)


@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    # 运行开发web服务器
    app.run(debug=True)