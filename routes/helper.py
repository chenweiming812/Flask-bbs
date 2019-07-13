import functools
import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for

from models.user import User
from utils import log

import json
import redis


cache_session = redis.StrictRedis()
cache_csrf_token = redis.StrictRedis()

def login_required(route_function):
    @functools.wraps(route_function)
    def f():
        u = current_user()
        if u is None:
            return redirect(url_for('index.index'))
        else:
            return route_function()
    return f

def csrf_required(f: object) -> object:
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']

        u = current_user()
        if cache_csrf_token.exists(token) and int(cache_csrf_token.get(token).decode()) == u.id:
            cache_csrf_token.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper

def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        id = int(cache_session.get(session_id).decode())
        u = User.one(id=id)
        return u
    else:
        u = User.one(id=-1)
        return u

def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    cache_csrf_token.set(token, u.id)
    return token

