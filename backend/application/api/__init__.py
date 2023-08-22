from flask import Blueprint 

users_bp = Blueprint('users', __name__, '/users')
auth_bp = Blueprint('auth', __name__, '/auth')
