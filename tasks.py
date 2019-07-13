from celery import Celery
from models.message import mailer

celery = Celery('tasks', backend='redis://localhost', broker='redis://localhost')

@celery.task(bind=True)
def send_async(self, subject, author, to, plain):
    try:
        m = mailer.new(
            subject=subject,
            author=author,
            to=to,
        )
        m.plain = plain
        mailer.send(m)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=3, max_retries=5)