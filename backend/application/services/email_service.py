from application import mail
from flask_mail import Message

def send_verification_email(self, user_email: str, token: str) -> None:
    pass