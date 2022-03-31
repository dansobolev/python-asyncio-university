import os
import asyncio
import datetime
import random
from typing import Union, List
from email.message import EmailMessage

import aiosmtplib
from aiosmtplib import SMTPResponseException
import jinja2

from app.config import Config


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(Config.BASE_DIR) + '/templates'),
    enable_async=True)


def send_email_message(message: EmailMessage,
                       send_to: Union[str, List[str]]):
    mail_upload_folder = './mails'
    if not os.path.isdir(mail_upload_folder):
        os.mkdir(mail_upload_folder)
    message['From'] = f'Admin'
    message['To'] = send_to
    try:
        now = datetime.datetime.now().strftime("%m-%d-0%Y--%H-%M-%S") + str(random.randrange(1, 1000))
        with open(f'{mail_upload_folder}/outgoing-{now}.eml', 'wb') as out:
            out.write(message.as_bytes())
    except SMTPResponseException:
        print("Error during email sending")
