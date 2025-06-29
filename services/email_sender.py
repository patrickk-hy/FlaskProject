from flask_mail import Mail, Message
from config import Config
import os

mail = Mail()


def init_mail(app):
    mail.init_app(app)


def send_email_with_attachment(recipient, subject, body, attachment_path):
    msg = Message(
        subject=subject,
        sender=Config.MAIL_USERNAME,
        recipients=[recipient]
    )
    msg.body = body

    with open(attachment_path, 'rb') as f:
        msg.attach(
            os.path.basename(attachment_path),
            'application/vnd.ms-excel',
            f.read()
        )

    mail.send(msg)