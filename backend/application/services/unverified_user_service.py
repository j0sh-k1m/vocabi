from application.models.models import UnverifiedUser
from application.data.unverified_user_dao import UnverifiedUserDAO
from application.data.user_dao import UserDAO
from application import Session 
from application.utils.custom_exceptions import UserAlreadyExistsException, UserDoesNotExistException
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from typing import Optional

class UnverifiedUserService:
    def __init__(self, unverified_user_dao: UnverifiedUserDAO, user_dao: UserDAO):
        self.unverified_user_dao = unverified_user_dao
        self.user_dao = user_dao

    def create_user(self, session: Session, first_name: str, last_name: str, email: str, password: bytes) -> None:
        """Creates an unverified user with provided credentials, upon signup/register
        
        Args:
            session: session
            first_name: user's first name
            last_name: user's last name
            email: user's email 
            password: user's (hashed) password 
        
        Raises:
            UserAlreadyExistsException: A user with provided email already exists
            InvalidEmailException: Email is invalid 
            InvalidPasswordException: Password does not meet the requirements  
        """
        try: 
            # check if user exists in database 
            if self.unverified_user_dao.get_user_by_email(session, email) is not None:
                raise UserAlreadyExistsException(email)
            
            if self.user_dao.get_user_by_email(session, email) is not None:
                raise UserAlreadyExistsException(email)

            # create new unverified user 
            new_unverified_user = UnverifiedUser(first_name, last_name, email, password)

            # add user to db 
            self.unverified_user_dao.add_user(session, new_unverified_user)

            #create token 
            user_id = self.unverified_user_dao.get_user_by_email(session, email).user_id
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = serializer.dumps(user_id, salt='email-verification')

            # set token on user 
            self.unverified_user_dao.set_user_token(session, user_id, token)

        except UserAlreadyExistsException:
            raise 

    def verify_user_token(self, session: Session, url_token: str) -> Optional[UnverifiedUser]:
        """Verifies the user by checking token value, and creates user in user table, and deletes user from unverified table
        
        Args: 
            session: session
            url_token: token from url params 
        
        Raises: 
            UserDoesNotExistException: user does not exist in table
        """
        try:
            user = session.query(UnverifiedUser).filter_by(token=url_token).first()
            if not user:
                raise UserDoesNotExistException       
            
            return user 

        except UserDoesNotExistException:
            raise UserDoesNotExistException('unverified_user')
        
    def delete_user(self, session, user_id: int) -> None:
        """Deletes a user from db
        
        Args: 
            session: session
            user_id: id of user to be deleted
        """
        self.unverified_user_dao.delete_user(session, user_id)
    