import os
import time

from celery import Celery
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail

sg = sendgrid.SendGridAPIClient(
    apikey=os.environ.get("SENDGRID_API_KEY")
)


load_dotenv(".env")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("REDIS_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


@celery.task(name="create_task")
def create_task(a, b, c):
    print('start')
    time.sleep(a)
    print('end')
    return b + c


@celery.task(name="send_email")
def send_email(to_email, subject, content):
    from_email = Email(os.environ.get("DEFAULT_EMAIL"))
    to_email = Email(to_email)
    content = Content(content)

    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    # The statements below can be included for debugging purposes
    print(response.status_code)
    print(response.body)
    print(response.headers)
