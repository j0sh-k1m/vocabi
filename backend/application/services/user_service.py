from application.models.models import User 
from application import Session 
import bcrypt 

class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.message = f"User with email {email} already exists"
        super().__init__(self.message)

class UserService: 

    def __init__(self, session):
        self.session = session 
