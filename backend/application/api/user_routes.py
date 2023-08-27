from flask import Blueprint, request, jsonify
from application import Session 
from flask_jwt_extended import jwt_required
from application.utils.custom_exceptions import MissingInformationException, UserDoesNotHaveAnyWordsException
from application.utils.serializers import serialize_user_words
from application.api import user_word_service

user_bp = Blueprint('user', __name__, url_prefix='/users')

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

# Get user statistics 
@user_bp.route('/<int:user_id>/statistics', methods=['GET'])
@jwt_required()
def get_user_statistics():
    pass

# Post user statistics 
@user_bp.route('/<int:user_id>/statistics', methods=['POST'])
@jwt_required()
def post_user_statistics():
    pass 

# TODO: Test jwt tokens 
# TODO: think of a way to handle POST requests. Should be able to pass any data that should be updated 
# TODO: come up with more specific endpoints for each of your pages 
# TODO: maybe create a settings table to store user settings data? 

# NOTE: WORDS
# get all user words 
# get all user words by category 
# post user words
# 