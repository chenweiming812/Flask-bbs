from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.board import Board
from routes import current_user

from models.topic import Topic
from routes.helper import new_csrf_token, csrf_required, login_required
from utils import log

main = Blueprint('gua_topic', __name__)


@main.route("/")
def index():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/index.html",user=u, ms=ms, token=token, bs=bs, bid=board_id)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))

@main.route("/delete")
@csrf_required
@login_required
def delete():
    u = current_user()
    id = int(request.args['id'])
    Topic.delete(id)
    return redirect(url_for('.index'))

@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", token=token, bs=bs, bid=board_id)

