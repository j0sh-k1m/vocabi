from application.models.models import User 
from application import Session 
from application.data.user_dao import UserDAO
import bcrypt 
from application.utils.custom_exceptions import UserAlreadyExistsException, InvalidEmailException, InvalidPasswordException
from application.utils.utils import is_valid_email, is_valid_password

class UserService: 
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao 

    def create_user(self, session: Session, first_name: str, last_name: str, email: str, password: str) -> None:
        """Creates a user in the user table with provided credentials/info
        
        Args:
            session: sqlalchemy.orm session
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