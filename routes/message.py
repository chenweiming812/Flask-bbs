from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.message import Messages
from routes.helper import login_required

main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    receiver_id = int(form['receiver_id'])
    Messages.send(
        title=form['title'],
        content=form['content'],
        sender_id=u.id,
        receiver_id=receiver_id
    )

    return redirect(url_for('.index'))


@main.route('/')
@login_required
def index():
    u = current_user()
    send = Messages.all(sender_id=u.id)
    received = Messages.all(receiver_id=u.id)
    t = render_template(
        'mail/index.html',
        send=send,
        received=received,
        user = u
    )
    return t


@main.route('/view/<int:id>')
def view(id):
    message = Messages.one(id=id)
    u = current_user()
    if u.id in [message.receiver_id, message.sender_id]:
        return render_template('mail/detail.html', message=message)
    else:
        return redirect(url_for('.index'))
