import abc 
from application.models.models import User, UserWord, UserStat
from typing import Optional

class UserDAO(abc.ABC):
    
    @abc.abstractmethod
    def add_user(self, session, user: User) -> None:
        raise NotImplementedError 
    
    @abc.abstractmethod 
    def get_user_by_id(self, session, id: int) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_email(self, session, email: str) -> Optional[User]: 
        raise NotImplementedError 
    
    @abc.abstractmethod
    def check_email(self, session, email: str) -> bool: 
        raise NotImplementedError
    
    @abc.abstractmethod
    def udpate_user_first_name(self, session, first_name: str) -> None:
        raise NotImplementedError 
    
    @abc.abstractmethod
    def update_user_last_name(self, session, last_name: str) -> None: 
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_user_email_verified(self, session, email: str, verified: bool) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def udpate_user_password(self, session, id: int, password: str) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_user(self, session, id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_vocab(self, session, id: int) -> Optional[UserWord]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_stats(self, session, id: int) -> Optional[UserStat]: 
        raise NotImplementedError
    

