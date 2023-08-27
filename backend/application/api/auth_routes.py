from flask import Blueprint, request, jsonify
from application import Session
from application.utils.custom_exceptions import UserAlreadyExistsException, InvalidEmailException, InvalidPasswordException, UserDoesNotExistException, InvalidLoginCredentialsException, MissingInformationException
from application.utils.utils import hash_password
from application.utils.utils import is_valid_email, is_valid_password
from flask_jwt_extended import create_access_token
from application.api import unverified_user_service, user_service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

"""User sign up"""
@auth_bp.route('/register', methods=['POST'])
def signup():
    try:
        print("Signing up...")
        data = request.json
        
        session = Session()

        if not data['first_name'] or not data['last_name'] or not data['email'] or not data['password']:
            raise MissingInformationException

        if not is_valid_email(data['email']):
            raise InvalidEmailException(data['email'])

        if not is_valid_password(data['password']):
            raise InvalidPasswordException

        print("Valid email & password")

        # Hash password 
        hashed_password = hash_password(data['password'])

        # Create new unverifified_user 
        unverified_user_service.create_user(
                    session, data['first_name'], data['last_name'], data['email'], hashed_password)  
          
        print("User created in unverified_user table")

        # Commit changes to db 
        session.commit()

        # TODO: Send verification email to user

        # Return a result message 
        return jsonify({ "message": f"Successfully created user: {data['email']} " }), 200
    
    except UserAlreadyExistsException as e:
        return jsonify({ "error": str(e) }), 400
    
    except InvalidEmailException as e:
        return jsonify({ "error": str(e) }), 400
    
    except InvalidPasswordException as e:
        return jsonify({ "error": str(e) }), 400
    
    except MissingInformationException as e: 
        return jsonify({ "error": str(e) }), 400
    
    except Exception as e: 
        # Handle exceptions 
        session.rollback() # Rollback (remove) changes 
        return jsonify({ "error": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close() 

"""Verify a user's account by email address"""
@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try: 
        session = Session()

        # verify the user
        user = unverified_user_service.verify_user_token(session, token)

        # create user in user table 
        user_service.create_user(session, user.first_name, user.last_name, user.email, user.password)

        # delete user from unverified_user table 
        unverified_user_service.delete_user(session, user.user_id)

        session.commit()

        return jsonify({ "message": f"Successfully verified {user.email}" }), 200 

    # handle errors 
    except UserDoesNotExistException as e:
        return jsonify({ "error": str(e) }), 400
    
    except UserAlreadyExistsException as e:
        return jsonify({ "error": str(e) }), 400 
    
    except InvalidEmailException as e:
        return jsonify({ "error": str(e) }), 400 
    
    except InvalidPasswordException as e: 
        return jsonify({ "error": str(e) }), 400 
    
    except Exception as e:
        session.rollback()
        return jsonify({ "error": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json 

        session = Session()

        if not data['email'] or not data['password']:
            raise MissingInformationException

        # check user input validity 
        if not is_valid_email(data['email']):
            raise InvalidEmailException

        if not is_valid_password(data['password']):
            raise InvalidPasswordException

        # attempt to login the user 
        user = user_service.user_login(session, data['email'], data['password'])

        # create access token NOTE: may want to change identity to email 
        access_token = create_access_token(identity=user.user_id)

        return jsonify({ "token": access_token }), 200

    except UserDoesNotExistException as e:
        return jsonify({ "error": str(e) }), 400

    except InvalidLoginCredentialsException as e:
        return jsonify({ "error": str(e) }), 400
    
    except InvalidEmailException as e:
        return jsonify({ "error": str(e) }), 400 
    
    except InvalidPasswordException as e:
        return jsonify({ "error": str(e) }), 400 

    except Exception as e: 
        session.rollback()
        return jsonify({ "error": f"Server of Database error: {e}" }), 500 
    
    finally:
        session.close()