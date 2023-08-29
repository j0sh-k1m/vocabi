import abc 
from application.models.models import UserStat
from typing import Optional, List 

class UserStatDAO(abc.ABC):

    @abc.abstractmethod
    def add_user_stat(self, session, user_stat: UserStat) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod 
    def delete_user_stat(self, session, user_id: int) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_stat_by_user_id(self, session, user_id: int) -> Optional[UserStat]: 
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_user_stat(self, session, user_id: int, changes: dict) -> None:
        raise NotImplementedError
    
class SQLAlchemyUserStatDAO(UserStatDAO):

    def add_user_stat(self, session, user_stat: UserStat) -> None: 
        """Add user stat to table
        
        Args:
            session: session 
            user_stat: user stats 
        """
        session.add(user_stat)
        session.flush() 

    def delete_user_stat(self, session, user_id: int) -> None:
        """Delete user stats
        
        Args: 
            session: session 
            user_id: id of the user 
        """
        user_stats = session.query(UserStat).filter_by(user_id=user_id).first() 
        session.delete(user_stats)
        session.commit()

    def get_stat_by_user_id(self, session, user_id: int) -> Optional[UserStat]:
        """Get a user's stats 
        
        Args:
            session: session 
            user_id: id of the user 
        """
        return session.query(UserStat).filter_by(user_id=user_id).first() 
    
    def update_user_stat(self, session, user_id: int, changes: dict) -> None:
        """Update a user word 
        
        Args: 
            session: session 
            user_id: id of the user
            changes: values to change 
        """
        user_stat = session.query(UserStat).filter_by(user_id=user_id).first() 
        for key, value in changes.items(): 
            if value is not None and hasattr(user_stat, key):
                setattr(user_stat, key, value)