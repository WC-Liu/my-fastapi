from asgiref.sync import async_to_sync
from celery import Celery

from app.utils.mail import create_message, mail

c_app = Celery()
c_app.config_from_object("app.core.config")


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):
    message = create_message(recipient=recipients, subject=subject, body=body)

    async_to_sync(mail.send_message)(message)
    print("邮件发送成功")
