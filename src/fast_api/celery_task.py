from celery import Celery
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fast_api.config import config

from fast_api.email import create_message, emailObj
from asgiref.sync import async_to_sync

c_app = Celery(__name__)
c_app.config_from_object("fast_api.config")


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):
    print("hai")
    message = create_message(recipients=recipients, subject=subject, body=body)
    async_to_sync(emailObj.send_message)(message)
    print("Email sent")
