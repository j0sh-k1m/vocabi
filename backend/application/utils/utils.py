import re 
import bcrypt
from flask_mail import Message, Mail
from flask import current_app
from application.models.models import UserWord
from math import pow
import random

def send_verification_email(user_email: str, token: str, mail: Mail) -> None:
    recipient = user_email 
    msg = Message("Vocabi - Verify your email", sender=current_app.config["MAIL_USERNAME"], recipients=[recipient])
    msg.body = f"""
        Hello,

        Thank you for registering with Vocabi. To complete your registration and verify your email address, copy this code and paste it:

        [Verification Code]: {token}

        If you did not register for a Vocabi account, please ignore this email.

        Best regards,
        The Vocabi Team
        """
    mail.send(msg)

def send_reset_password_email(user_email: str, token: str, mail: Mail) -> None: 
    recipient = user_email 
    msg = Message("Vocabi - Reset Your Password", sender=current_app.config["MAIL_USERNAME"], recipients=[recipient])

    msg.body = f"""
        Hello

        You have made a request to reset your password. To complete this process verify your email address by copying and pasting this code: 

        [Verification Code]: {token}
    """
    mail.send(msg)

def is_valid_password(password: str) -> bool: 
    """Checks for password validity. Length of 8, 1 upper/lowercase, special char, digit
    
    Args:
        password: password to be checked
    
    Returns:
        type: bool validity of password
    """
    uppercase_regex = r'[A-Z]'
    lowercase_regex = r'[a-z]'
    digit_regex = r'\d'
    special_char_regex = r'[!@#$%^&*()\-_=+[\]{}|;:,<>.?/]'

    return (re.search(uppercase_regex, password) is not None and 
            re.search(lowercase_regex, password) is not None and 
            re.search(digit_regex, password) is not None and 
            re.search(special_char_regex, password) is not None
            and len(password) >= 8)

def is_valid_email(email: str) -> bool:
    """Checks an email for validity
    
    Args:
        email: email to be checked
    
    Returns:
        type: bool validity of email
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def hash_password(password: str) -> bytes:
    # hash password 
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def hash_string(string: str) -> bytes: 
    """Hashes a string
    
    Args: 
        string: string to be hashed 
    """
    return bcrypt.hashpw(string.encode('utf-8'), bcrypt.gensalt())

def check_hashed_string(string: str, hashed_string: bytes) -> bool:
    """Check a hashed string to a regular string
    
    Args:
        string: original string 
        hashed_string: hashed string
    """
    return bcrypt.checkpw(string.encode(), hashed_string)

def calculate_word_score(word: UserWord) -> float:
    """Caluclates a 'score' of a word based on attempts and accuracy

    Formula: [(total_attempts) ^ (1/6)] / accuracy + (0 <= num < 1)
    
    Args: 
        word: the word to calculate the score for 
    """

    total_attempts = float(word['correct']) + float(word['incorrect'])

    if total_attempts == 0:
        return float('inf')

    accuracy = float(word['correct']) / float(total_attempts)

    if accuracy == 0: 
        return float('inf')
    
    root_of_attempts = pow(total_attempts, 1/6)

    score = root_of_attempts / accuracy

    score += random.random()

    return score 