from flask import Blueprint, request, jsonify
from application import Session 
from flask_jwt_extended import jwt_required
from application.utils.custom_exceptions import MissingInformationException, UserDoesNotHaveAnyWordsException
from application.utils.serializers import serialize_user_words
from application.api import user_word_service

user_bp = Blueprint('user', __name__, url_prefix='/users')

# NOTE: this is for user information (Settings etc)

# Get user information 
@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_info():
    pass

# Post user information
@user_bp.route('/<int:user_id>', methods=['POST'])
@jwt_required() 
def post_user_info(): 
    pass

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    pass 