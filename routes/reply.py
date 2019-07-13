from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.message import Messages
from models.user import User
from routes import current_user

from models.reply import Reply
from routes.index import cache

main = Blueprint('gua_reply', __name__)

def users_from_content(content):
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            print('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users

def send_mails(sender, receivers, reply_link, reply_content):
    content = '链接：{}\n内容：{}'.format(
        reply_link,
        reply_content
    )
    for r in receivers:
        title = '你被 {} AT 了'.format(sender.username)
        Messages.send(
            title=title,
            content=content,
            sender_id=sender.id,
            receiver_id=r.id
        )

@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()

    content = form['content']
    users = users_from_content(content)
    send_mails(u, users, request.referrer, content)

    form = form.to_dict()
    m = Reply.add(form, user_id=u.id)

    k = 'topic_join_all_{}'.format(u.id)
    cache.delete(k)
    return redirect(url_for('gua_topic.detail', id=m.topic_id))

