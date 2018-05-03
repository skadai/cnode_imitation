from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.mail import Mail

main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    form['receiver_id'] = int(form['receiver_id'])
    u = current_user()
    m = Mail.new(form, sender_id=u.id)
    return redirect(url_for('.index'))


@main.route('/')
def index():
    u = current_user()

    sent_mail = Mail.find_all(sender_id=u.id)
    received_mail = Mail.find_all(receiver_id=u.id)

    t = render_template(
        'mail/index.html',
        send=sent_mail,
        received=received_mail,
    )
    return t


@main.route('/view/<int:id>')
def view(id):
    mail = Mail.find_by(id=id)
    u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    if u.id in [mail.receiver_id, mail.sender_id]:
        return render_template('mail/detail.html', mail=mail)
    else:
        return redirect(url_for('.index'))
