import abc
from application.models.models import ResetPassword
from typing import Optional

class ResetPasswordDAO(abc.ABC):

    @abc.abstractmethod
    def add_user(self, session, user: ResetPassword) -> None:
        raise NotImplementedError

    @abc.abstractmethod 
    def delete_user(self, session, email: str) -> None: 
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, session, email: str) -> Optional[ResetPassword]: 
        raise NotImplementedError


class SQLAlchemyResetPasswordDAO(ResetPasswordDAO):

    def add_user(self, session, user: ResetPassword) -> None: 
        """Adds a user to the reset password table 
        
        Args:
            session: session 
            user: user to add to the reset password table 
        """
        session.add(user)
        session.flush() 
    
    def delete_user(self, session, email: str) -> None: 
        """Deletes a user from the reset password table 
        
        Args: 
            session: session 
            user: user to delete from the ResetPassword table 
        """
        user_to_delete = session.query(ResetPassword).filter_by(email=email).first() 
        session.delete(user_to_delete)

    def get_user(self, session, email: str) -> Optional[ResetPassword]: 
        """Gets a user from the reset password table
        
        Args: 
            session: session 
            user_id: id of the user to get 
        """
        return session.query(ResetPassword).filter_by(email=email).first()
        