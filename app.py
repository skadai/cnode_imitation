from flask import Flask
import time
import config

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.mail import main as mail_routes
from utils import log


def count(input):
    log('count using jinja filter')
    return len(input)


def fromnow(lasttime):
    return (int(time.time())-lasttime)//86400


def sort_fromnow(topics):
    topics.sort(key=lambda x:x.updated_time, reverse=True)
    return topics


def message_in(mail):
    if '@' in mail.title:
        return '你被{} @了'.format(mail.sender())
    else:
        return mail.title


def message_out(mail):
    if '@' in mail.title:
        return '你@了 {}'.format(mail.receiver())
    else:
        return mail.title


def configured_app():
    # web framework
    # web application
    # __main__
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = config.secret_key
    register_routes(app)

    app.add_template_filter(count)
    app.add_template_filter(fromnow)
    app.add_template_filter(sort_fromnow)
    app.add_template_filter(message_out)
    app.add_template_filter(message_in)

    return app


def register_routes(app):
    """
    在 flask 中，模块化路由的功能由 蓝图（Blueprints）提供
    蓝图可以拥有自己的静态资源路径、模板路径（现在还没涉及）
    用法如下
    """
    # 注册蓝图
    # 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # 自动 reload jinja
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
    )
    app.run(**config)
