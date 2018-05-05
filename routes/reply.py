from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)
from models.reply import ReplySQL as Reply
from routes import (
    current_user,
    login_required
)


main = Blueprint('reply', __name__)


@main.route("/add", methods=["POST"])
@login_required
def add():
    form = request.form.to_dict()
    u = current_user()
    print('DEBUG', form)
    form['user_id'] = u.id
    m = Reply.new(**form)
    m.add_mail()

    return redirect(url_for('topic.detail', id=m.topic_id))



