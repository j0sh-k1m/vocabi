from flask import Blueprint 
from application.data.user_dao import SQLAlchemyUserDAO
from application.data.unverified_user_dao import SQLAlchemyUnverifiedUserDAO
from application.data.user_word_dao import SQLAlchemyUserWordDAO
from application.data.user_stat_dao import SQLAlchemyUserStatDAO
from application.data.reset_password_dao import SQLAlchemyResetPasswordDAO

from application.services.user_service import UserService
from application.services.unverified_user_service import UnverifiedUserService
from application.services.user_word_service import UserWordService
from application.services.user_stat_service import UserStatService
from application.services.auth_service import AuthService

from flask import current_app as app 
from flask_mail import Mail 

mail = Mail(app)

# Init DAOs 
user_dao = SQLAlchemyUserDAO()
unverified_user_dao = SQLAlchemyUnverifiedUserDAO()
user_word_dao = SQLAlchemyUserWordDAO()
user_stat_dao = SQLAlchemyUserStatDAO()
reset_password_dao = SQLAlchemyResetPasswordDAO()

# Init Services 
user_service = UserService(user_dao=user_dao)
unverified_user_service = UnverifiedUserService(unverified_user_dao=unverified_user_dao, user_dao=user_dao)
user_word_service = UserWordService(user_word_dao=user_word_dao)
user_stat_service = UserStatService(user_stat_dao=user_stat_dao)
auth_service = AuthService(reset_password_dao=reset_password_dao)