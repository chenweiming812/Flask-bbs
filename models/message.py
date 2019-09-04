from sqlalchemy import Column, Unicode, UnicodeText, Integer
import tasks
from config import admin_mail
from models.base_model import SQLMixin, db
from models.user import User

def send_mail(subject, author, to, content):
    m = tasks.mailer.new(
        subject=subject,
        author=author,
        to=to,
    )
    m.plain = content
    tasks.mailer.send(m)


class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    @staticmethod
    def send(title: str, content: str, sender_id: int, receiver_id: int):
        form = dict(
            title=title,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id
        )

        Messages.new(form)
        receiver: User = User.one(id=receiver_id)

        tasks.send_async.delay(
            subject=title,
            author=admin_mail,
            to=receiver.email,
            plain='站内信通知：\n {}'.format(content),
        )

