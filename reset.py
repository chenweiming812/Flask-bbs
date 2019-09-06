from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        secret.database_password
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS cwm')
        c.execute('CREATE DATABASE cwm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE cwm')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='cwm',
        password='123',
        email='chenweiming812@outlook.com'
    )
    u = User.register(form)

    form = dict(
        username='cwmcwm',
        password='123',
        email='chenweiming812@outlook.com'
    )
    u = User.register(form)

    form = dict(
        title='all'
    )
    b = Board.new(form)
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form = dict(
        title='markdown demo',
        board_id=b.id,
        content=content
    )

    for i in range(10):
        print('begin topic <{}>'.format(i))
        t = Topic.add(topic_form, u.id)

        reply_form = dict(
            content='I am Iron Man',
            topic_id=t.id,
        )
        for j in range(5):
            Reply.add(reply_form, u.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
