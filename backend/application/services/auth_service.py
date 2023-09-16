from application.models.models import ResetPassword
from application.data.reset_password_dao import ResetPasswordDAO
from typing import Optional
from datetime import datetime

class AuthService: 
    def __init__(self, reset_password_dao: ResetPasswordDAO):
        self.reset_password_dao = reset_password_dao

    def create_reset_password(self, session, token: bytes, email: str):
        """Creates a reset password item in the table 
        
        Args: 
            session: session 
            token: hashed token
            email: user's email
        """
        new_reset_password = ResetPassword(token=token, email=email)
        self.reset_password_dao.add_user(session, new_reset_password)

    def get_reset_password_by_email(self, session, email: str) -> Optional[ResetPassword]: 
        """Gets a user by user_id 
        
        Args: 
            session: sesison 
            email: user's email 
        """
        return self.reset_password_dao.get_user(session=session, email=email)
    
    def update_reset_password(self, session, email: str, token: bytes) -> None: 
        """Updates an existing request to reset passwor d
        
        Args: 
            session: session 
            email: user's email 
            token: new token
        """
        user = self.reset_password_dao.get_user(session=session, email=email)
        if hasattr(user, 'token'):
            setattr(user, 'token', token)

        if hasattr(user, 'current_date'):
            setattr(user, 'current_date', datetime.utcnow())

    def delete_reset_password(self, session, email: str): 
        """Deletes a reset password request
        
        Args:
            session: session
            email: user email
        """
        self.reset_password_dao.delete_user(session, email)