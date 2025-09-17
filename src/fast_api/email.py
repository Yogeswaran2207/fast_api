

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List
import os
from fast_api.config import config
from fastapi_mail import MessageType

config_obj = ConnectionConfig(
    MAIL_USERNAME = config.MAIL_USERNAME,
    MAIL_PASSWORD = config.MAIL_PASSWORD,
   
    MAIL_FROM = config.MAIL_FROM,
    MAIL_PORT = config.MAIL_PORT,
    MAIL_SERVER = config.MAIL_SERVER,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True
)   
print(config.MAIL_PASSWORD)
emailObj = FastMail(config_obj)



def create_message(recipients: list[str], subject: str, body: str):

    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )

    return message