from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.topic import TopicSQL as Topic
from models.board import BoardSQL as Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    hots = Topic.hots()
    if board_id == -1:
        ms = Topic.all(deleted=0)
    else:
        # ms = Topic.find_all(board_id=board_id)
        ms = Topic.all(board_id=board_id,deleted=0)

    token = new_csrf_token()
    bs = Board.all()
    user = current_user()
    return render_template("topic/index.html", ms=ms, token=token,
                            bs=bs, bid=board_id, user=user, hots=hots)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m,
                           user=current_user(),hots=Topic.hots())


@main.route("/delete")
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id', -1))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id,
                           hots=Topic.hots(), user=current_user())


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    form['user_id'] = u.id
    Topic.new(**form)
    return redirect(url_for('.index'))
