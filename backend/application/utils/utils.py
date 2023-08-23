import re 
import bcrypt

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

def hash_password(password: str) -> str:
    # hash password 
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())