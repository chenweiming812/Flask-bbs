import os
import random
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory)
from werkzeug.datastructures import FileStorage

from config import admin_mail
from models import topic, reply
from models.message import send_mail
from models.topic import Topic
from models.user import User
from routes.helper import new_csrf_token, cache_session, current_user
from tasks import send_async

from utils import log
import json
import redis

cache = redis.StrictRedis()
main = Blueprint('index', __name__)

@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    progress_register = '恭喜您，{}已经注册成功'.format(form['username'])
    return render_template('index.html',progress_register=progress_register)

@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login user <{}>'.format(u))
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('.index'))
    else:
        session_id = str(uuid.uuid4())
        cache_session.set(session_id, u.id)
        reps = redirect(url_for('gua_topic.index'))
        reps.set_cookie('session_id', session_id)
        return reps

def topic_all(id):
    ts = topic.Topic.all(user_id=id)
    return ts

def topic_join_all(id):
    k = 'topic_join_all_{}'.format(id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        return ts
    else:
        rs = reply.Reply.all(user_id=id)
        t_join = []
        for r in rs:
            t = topic.Topic.one(id=r.topic_id)
            if t not in t_join:
                t_join.append(t)
        v = json.dumps([t.json() for t in t_join])
        cache.set(k, v)
        return t_join

@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        ts = topic_all(u.id)
        t_join = topic_join_all(u.id)
        return render_template('profile.html', user=u, topic=ts, topic_join=t_join)


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        ts = topic.Topic.all(user_id=u.id)
        rs = reply.Reply.all(user_id=u.id)
        t_join = []
        for r in rs:
            t = topic.Topic.one(id=r.topic_id)
            if t not in t_join:
                t_join.append(t)
        return render_template('profile.html', user=u, topic=ts, topic_join=t_join)

@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)


token_dict = dict()
@main.route('/reset/send', methods=['POST'])
def reset_send():
    username = request.form['username']
    u = User.one(username=username)
    token = str(uuid.uuid4())
    token_dict[token] = u.id
    subject = '更改密码'
    author = admin_mail
    to = u.email
    content = '点击以下链接重置密码 http://152.136.46.27/reset/view?token={}'.format(token)
    send_async.delay(subject, author, to, content)
    progress_reset = '改更密码链接已经发送到您的邮件'
    return render_template('index.html',progress_reset=progress_reset)

@main.route('/reset/view')
def reset_view():
    if 'token' in request.args.keys():
        token = request.args['token']
        return render_template('password.html', token=token)
    else:
        progress = '申请失败，用户不存在'
        return render_template('index.html',progress=progress)

@main.route('/reset/update', methods=['POST'])
def reset_update():
    if 'token' in request.args.keys():
        token = request.args['token']
        id = token_dict[token]
        u = User.one(id=id)
        np = request.form['password']
        u.password = u.salted_password(np)
        u.save()
        progress_reset = '密码更改成功'
        return render_template('index.html',progress_reset=progress_reset)
    else:
        progress_reset = '密码更改失败'
        return render_template('index.html',progress_reset=progress_reset)

def not_found(e):
    return render_template('404.html')
