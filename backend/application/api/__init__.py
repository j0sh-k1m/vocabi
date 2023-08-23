from flask import Blueprint 
from application.data.user_dao import SQLAlchemyUserDAO
from application.data.unverified_user_dao import SQLAlchemyUnverifiedUserDAO

from application.services.user_service import UserService
from application.services.unverified_user_service import UnverifiedUserService

# Flask Blueprints 
users_bp = Blueprint('users', __name__, url_prefix='/users')


# Init DAOs 
user_dao = SQLAlchemyUserDAO()
unverified_user_dao = SQLAlchemyUnverifiedUserDAO()

# Init Services 
user_service = UserService(user_dao=user_dao)
unverified_user_service = UnverifiedUserService(unverified_user_dao=unverified_user_dao, user_dao=user_dao)