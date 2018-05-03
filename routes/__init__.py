import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for

from models.user import User
from utils import log

def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    if 'user_id' in session:
        uid = int(session['user_id'])
        # e = User.exist(id=uid)
        e = User.find_by(id=uid)
        if e:
            return e
            # return User.one(id=uid)
        else:
            return None
    else:
        return None



csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        u = current_user()
        if token in csrf_tokens and csrf_tokens[token] == u.id:
            csrf_tokens.pop(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    if u is not None:
        csrf_tokens[token] = u.id
    return token


def login_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    @wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u is None:
            log('游客用户')
            return redirect(url_for('index.index'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f
