from application.models.models import UserStat 
from application.data.user_stat_dao import UserStatDAO
from application import Session 
from typing import Optional 


class UserStatService:
    def __init__(self, user_stat_dao: UserStatDAO):
        self.user_stat_dao = user_stat_dao

    def create_user_stat(self, session: Session, user_id: int) -> None:
        """Create user stats 
        
        Args: 
            session: session
            user_id: id of the user 
        """
        user_stats = UserStat(user_id)
        self.user_stat_dao.add_user_stat(session, user_stats)

    def get_user_stat(self, session: Session, user_id: int) -> Optional[UserStat]:
        """Gets a user's stats
        
        Args: 
            session: session 
            user_id: id of the user 
        """
        return self.user_stat_dao.get_stat_by_user_id(session, user_id)
    
    def delete_user_stat(self, session: Session, user_id: int) -> None:
        """Delete a user's stats
        
        Args:
            session: session 
            user_id: id of the user
        """
        self.user_stat_dao.delete_user_stat(session, user_id)

    def update_user_stat(self, session: Session, user_id: int, changes: dict) -> None:
        """Update a user's statistics 
        
        Args: 
            session: session 
            user_id: a user's id 
            changes: user stat changes 
        """
        self.user_stat_dao.update_user_stat(session, user_id, changes)