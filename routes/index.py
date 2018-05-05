import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory
)

from routes import login_required
from models.user import UserSQL as User
from models.topic import TopicSQL as Topic
from utils import log

main = Blueprint('index', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    # u = User.find_by(id=uid)
    u = User.one(id=uid)
    return u



"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    session['user_id'] = 0
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    # form = request.args
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        log('登录失败')
        return redirect(url_for('topic.index'))
    else:
        log('登录成功')
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


@main.route('/user/<int:id>')
def user_detail(id):
    # u = User.find_by(id=id)
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        return render_template('profile.html', user=u)


@main.route('/user/<username>')
def user_profile(username):
    # u = User.find_by(username=username)
    u = User.one(username=username)
    if u is None:
        abort(404)
    else:
        # topics = Topic.find_all(user_id=u.id)
        topics = Topic.all(user_id=u.id)
        reply_topic = Topic.user_participated(u)
        return render_template('user.html', user=u,
                               reply_topic=reply_topic,topics=topics,
                               hots=Topic.hots(),u=current_user())


@main.route('/image/add', methods=['POST'])
@login_required
def image_add():
    file = request.files['avatar']

    # ../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    u.image = '/images/{}'.format(filename)
    # u.save()
    User.update(u.id, image=u.image)

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)


@main.route('/setting')
@login_required
def settings():
    u = current_user()
    return render_template('settings.html', user=u)


@main.route('/setting/change_info', methods=['POST'])
@login_required
def change_info():
    form = request.form.to_dict()
    u = current_user()
    # u.update(form)
    User.update(u.id, **form)
    return redirect(url_for('.settings'))


@main.route('/setting/change_password', methods=['POST'])
@login_required
def change_password():
    old_pass = request.form['old_pass']
    new_pass = request.form['new_pass']
    u = current_user()
    if u.password == u.salted_password(old_pass):
        # u.password = u.salted_password(new_pass)
        # u.save()
        password = u.salted_password(new_pass)
        User.update(u.id, password=password)
        msg = '密码更新成功'
    else:
        msg = '密码更新失败'
    return render_template('settings.html', user=u, msg=msg)
# def blueprint():
#     main = Blueprint('index', __name__)
#     main.route("/")(index)
#     main.route("/register", methods=['POST'])(register)
#     main.route("/login", methods=['POST'])(login)
#     main.route('/profile')(profile)
#     main.route('/user/<int:id>')(user_detail)
#
#     return main
