from flask import session, request

from models.user import User
from routes.helper import cache_session

from utils import log

def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        id = int(cache_session.get(session_id).decode())
        u = User.one(id=id)
        return u
    else:
        u = User.one(id=-1)
        return u
