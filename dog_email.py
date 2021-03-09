# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import secrets
from database import get_dog_by_handle, reset_database_password
import random
import string
from werkzeug.security import generate_password_hash

def send_message(handle, subject, body):

    dog = get_dog_by_handle('melba')
    name = dog['Name']
    email = dog['Email']

    message = Mail(
        from_email='epischooldemo@outlook.com',
        to_emails=email,
        subject=subject,
        html_content=body)
    try:
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(secrets.sendgrid_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def reset_password(handle):
    new_password = get_random_string(20)
    password_hash = generate_password_hash(new_password)
    print(password_hash)
    reset_database_password(handle, password_hash)
    send_message(handle, 'Dogchat password reset', 'Your new password is %s' % new_password)
