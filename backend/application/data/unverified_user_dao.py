import abc
from application.models.models import UnverifiedUser 
from typing import Optional

class UnverifiedUserDAO(abc.ABC):

    @abc.abstractmethod
    def add_user(self, session, user: UnverifiedUser) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_user(self, session, user_id: int) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user_by_token(self, session, user: UnverifiedUser) -> Optional[UnverifiedUser]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user_by_email(self, session, email: str) -> Optional[UnverifiedUser]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def set_user_token(self, session, user_id: int, token: str) -> None:
        raise NotImplementedError
    
class SQLAlchemyUnverifiedUserDAO(UnverifiedUserDAO):

    def add_user(self, session, user: UnverifiedUser) -> None:
        """Adds the user to unverified user table 
        
        Args:
            session: sqlalchemy.orm session
            user: UnverifiedUser to add to db 
        """
        session.add(user)
        session.flush()
    
    def delete_user(self, session, user_id: int) -> None:
        """Deletes user from unverified user table
        
        Args: 
            session: sqlalchemy.orm session
            user_id: Unverified user_id to delete from db 
        """
        user_to_delete = session.query(UnverifiedUser).filter_by(user_id=user_id).first()
        session.delete(user_to_delete)
    
    def get_user_by_token(self, session, token: str) -> Optional[UnverifiedUser]:
        """Gets user by token
        
        Args:
            session: sqlalchemy.orm session 
            token: token from verification email 
        """
        return session.query(UnverifiedUser).filter_by(token=token).first()
    
    def get_user_by_email(self, session, email: str) -> Optional[UnverifiedUser]:
        """Gets an unverified user by email
        
        Args: 
            session: sqlalchemy.orm session
            email: user's email 
        """
        return session.query(UnverifiedUser).filter_by(email=email).first()
    
    def set_user_token(self, session, user_id: int, token: str) -> None:
        """Sets the email verification token 
        
        Args: 
            session: sqlaclhemy.orm session 
            token: token to be set 
        """
        session.query(UnverifiedUser).filter_by(user_id=user_id).update({ 'token': token })