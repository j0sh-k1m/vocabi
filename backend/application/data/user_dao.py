import abc
from application.models.models import User
from typing import Optional

class UserDAO(abc.ABC):
    
    @abc.abstractmethod
    def add_user(self, session, user: User) -> None:
        raise NotImplementedError 
    
    @abc.abstractmethod 
    def get_user_by_id(self, session, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_email(self, session, email: str) -> Optional[User]: 
        raise NotImplementedError 
    
    @abc.abstractmethod
    def update_user_first_name(self, session, first_name: str) -> None:
        raise NotImplementedError 
    
    @abc.abstractmethod
    def update_user_last_name(self, session, last_name: str) -> None: 
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_user_password(self, session, email: str, password: bytes) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_user(self, session, user_id: int) -> None:
        raise NotImplementedError
    

class SQLAlchemyUserDAO(UserDAO):
    
    def add_user(self, session, user: User) -> None:      
        """Adds user to the User table in database

        Args: 
            session: sqlalchemy.orm Session 
            user: User to add to the database
        """
        session.add(user)
        session.flush()

    def get_user_by_id(self, session, user_id: int) -> Optional[User]:
        """Gets the user by id 

        Args:
            session: sqlalchemy.orm session 
            user_id: id of user 
        """
        return session.query(User).filter_by(user_id=user_id).first() 
    
    def get_user_by_email(self, session, email: str) -> Optional[User]:
        """Gets the user by email 

        Args: 
            session: sqlalchemy.orm session
            email: email of user 
        """
        return session.query(User).filter_by(email=email).first() 
    
    def update_user_first_name(self, session, user_id: int, first_name: str) -> None: 
        """Update a user's first name

        Args:
            session: sqlalchemy.orm session 
            user_id: id of the user 
            first_name: udpated first_name 
        """
        session.query(User).filter_by(user_id=user_id).update({ 'first_name': first_name })

    def update_user_last_name(self, session, user_id: int, last_name: str) -> None:
        """Update a user's last name

        Args:
            session: sqlalchemy.orm session 
            user_id: id of the user 
            last_name: updated last name 
        """
        session.query(User).filter_by(user_id=user_id).update({ 'last_name': last_name })

    def update_user_password(self, session, email: str, password: bytes) -> None: 
        """Update a user's password, Does not check for correct password 

        Args:
            session: sqlalchemy.orm session 
            user_id: id of user 
            password: hashed password of user 
        """
        session.query(User).filter_by(email=email).update({ 'password': password })

    def delete_user(self, session, user_id: int) -> None:
        """Delete user from database 
        
        Args:
            session: sqlalchemy.orm session 
            user_id: id of user 
        """
        user_to_delete = session.query(User).filter_by(user_id=user_id).first() 
        session.delete(user_to_delete)
        session.commit()