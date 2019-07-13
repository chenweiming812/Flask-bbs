import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    send_from_directory)
from werkzeug.datastructures import FileStorage

from models.board import Board
from models.user import User
from routes import current_user

from models.topic import Topic
from routes.helper import new_csrf_token, csrf_required, login_required

main = Blueprint('gua_setting', __name__)

@main.route("/")
def index():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    return render_template("setting.html", user=u, bid=board_id)

@login_required
@main.route("/signature", methods=['POST'])
def signature():
    u = current_user()
    signature = request.form['signature']
    u.signature = signature
    u.save()
    return render_template("setting.html", user=u)

@login_required
@main.route("/password", methods=['POST'])
def password():
    u = current_user()
    op = request.form['old_password']
    op = u.salted_password(op)
    np = request.form['new_password']

    if op == u.password:
        u.password = u.salted_password(np)
        u.save()
        result = '密码更新成功'
    else:
        result = '密码更新错误'

    return render_template("setting.html", user=u, result=result)

@login_required
@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    filename = str(uuid.uuid4())
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.index'))




