from flask import Blueprint 
from application.data.user_dao import SQLAlchemyUserDAO
from application.data.unverified_user_dao import SQLAlchemyUnverifiedUserDAO
from application.data.user_word_dao import SQLAlchemyUserWordDAO

from application.services.user_service import UserService
from application.services.unverified_user_service import UnverifiedUserService
from application.services.user_word_service import UserWordService

# Flask Blueprints 
users_bp = Blueprint('users', __name__, url_prefix='/users')


# Init DAOs 
user_dao = SQLAlchemyUserDAO()
unverified_user_dao = SQLAlchemyUnverifiedUserDAO()
user_word_dao = SQLAlchemyUserWordDAO()

# Init Services 
user_service = UserService(user_dao=user_dao)
unverified_user_service = UnverifiedUserService(unverified_user_dao=unverified_user_dao, user_dao=user_dao)
user_word_service = UserWordService(user_word_dao=user_word_dao)
