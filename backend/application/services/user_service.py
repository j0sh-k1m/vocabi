from application.models.models import User 
from application import Session 
from application.data.user_dao import UserDAO
from application.utils.custom_exceptions import UserAlreadyExistsException, UserDoesNotExistException, InvalidLoginCredentialsException
from application.utils.utils import is_valid_email, is_valid_password
from typing import Optional
import bcrypt

class UserService: 
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao 

    def create_user(self, session: Session, first_name: str, last_name: str, email: str, password: bytes) -> None:
        """Creates a user in the user table with provided credentials/info
        
        Args:
            session: session
            first_name: users first name
            last_name: users last name
            email: users email
            password: users password 
        
        Raises:
            UserAlreadyExistsException: A user with the provided email already exists 
            InvalidEmailException: User's email in invalid 
            InvalidPasswordException: User's password does not meet password requirements 
        """ 
        
        try: 
            if self.user_dao.get_user_by_email(session, email) is not None: 
                raise UserAlreadyExistsException(email)

            new_user = User(first_name, last_name, email, password)

            self.user_dao.add_user(session, new_user)

        # propogate exceptions to API
        except UserAlreadyExistsException:
            raise
    
    def get_user_info_by_id(self, session, user_id: int) -> Optional[User]:
        """Gets user by id 
        
        Args: 
            session: session
            user_id: user's id
        """
        return self.user_dao.get_user_by_id(session, user_id)
    
    def get_user_info_by_email(self, session, email: str) -> Optional[User]:
        """Gets user by email 
        
        Args:
            session: sqlalchemy.orm session
            email: user's email 
        """
        return self.user_dao.get_user_by_email(session, email)
    
    def user_login(self, session, email: str, password: bytes) -> Optional[User]:
        """Attempts to login user
        
        Args: 
            session: session
            email: user's email
            password: user's password
        
        Raises: 
            UserDoesNotExistException: user does not exist in database 
            InvalidLoginCredentialsException: user has not provided proper credentials 
        """
        try:
            user = self.user_dao.get_user_by_email(session, email)
            if user is None:
                raise UserDoesNotExistException

            if bcrypt.checkpw(password.encode(), user.password) is False:
                raise InvalidLoginCredentialsException

            return user 

        except UserDoesNotExistException: 
            raise UserDoesNotExistException
        
        except InvalidLoginCredentialsException:
            raise InvalidLoginCredentialsException
        
    def update_password(self, session, email: str, password: bytes) -> None: 
        """Updates a user's password
        
        Args: 
            session: session 
            user_id: id of the user 
            password: new password 
        """
        self.user_dao.update_user_password(session=session, email=email, password=password)