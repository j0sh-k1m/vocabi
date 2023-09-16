from flask import Blueprint, current_app, request, jsonify
from itsdangerous import Serializer, URLSafeTimedSerializer
from application import Session
from application.utils.custom_exceptions import UserAlreadyExistsException, InvalidEmailException, InvalidPasswordException, UserDoesNotExistException, InvalidLoginCredentialsException, MissingInformationException, EmailSendingFailedException, InvalidTokenException
from application.utils.utils import hash_password, is_valid_email, is_valid_password, send_verification_email, send_reset_password_email, hash_string, check_hashed_string
from flask_jwt_extended import create_access_token
from application.api import unverified_user_service, user_service, user_stat_service, auth_service
from application.utils.serializers import serialize_user
from flask_mail import Message
from application.api import mail

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

"""User sign up"""
@auth_bp.route('/register', methods=['POST'])
def signup():
    try:
        data = request.json
        
        session = Session()

        if data.get('first_name') is None or data.get('last_name') is None or data.get('email') is None or data.get('password') is None: 
            raise MissingInformationException

        if not is_valid_email(data['email']):
            raise InvalidEmailException(data['email'])

        if not is_valid_password(data['password']):
            raise InvalidPasswordException

        # Hash password 
        hashed_password = hash_password(data['password'])

        # Create new unverifified_user 
        unverified_user_service.create_user(
                    session, data['first_name'], data['last_name'], data['email'], hashed_password)  

        unverified_user = unverified_user_service.get_user_by_email(session, data['email'])

        # Commit changes to db 
        session.commit()

        try: 
            send_verification_email(unverified_user.email, unverified_user.token, mail)
        
        except EmailSendingFailedException:
            raise EmailSendingFailedException

        # Return a result message 
        return jsonify({ "message": f"Successfully created user: {data['email']}", "token": unverified_user.token }), 200
    
    except EmailSendingFailedException as e: 
        return jsonify({ "message": str(e) }), 400 
    
    except UserAlreadyExistsException as e:
        session.rollback() 
        return jsonify({ "message": str(e) }), 400
    
    except InvalidEmailException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400
    
    except InvalidPasswordException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400
    
    except MissingInformationException as e: 
        session.rollback()
        return jsonify({ "message": str(e) }), 400
    
    except Exception as e: 
        # Handle exceptions 
        session.rollback() # Rollback (remove) changes 
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close() 

"""Verify a user's account by email address"""
@auth_bp.route('/email-verification', methods=['POST'])
def verify_email():
    try: 
        session = Session()

        data = request.json 

        token = data.get('token')
        if token is None: 
            raise MissingInformationException

        # verify the user
        user = unverified_user_service.verify_user_token(session, token)

        print("User token verified")

        # create user in user table 
        user_service.create_user(session, user.first_name, user.last_name, user.email, user.password)

        print("Created user in user table")

        # delete user from unverified_user table 
        unverified_user_service.delete_user(session, user.user_id)

        print("delete in unverified")

        # create stats table for user 
        user_stat_service.create_user_stat(session, user.user_id)

        session.commit()

        return jsonify({ "message": f"Successfully verified {user.email}" }), 200 
    
    except MissingInformationException as e: 
        session.rollback()
        return jsonify({ "message": str(e) }), 400 

    # handle errors 
    except UserDoesNotExistException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400
    
    except UserAlreadyExistsException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400 
    
    except InvalidEmailException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400 
    
    except InvalidPasswordException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400 
    
    except Exception as e:
        session.rollback()
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json 

        session = Session()

        if data['email'] is None or data['password'] is None:
            raise MissingInformationException

        # check user input validity 
        if not is_valid_email(data['email']):
            raise InvalidLoginCredentialsException

        if not is_valid_password(data['password']):
            raise InvalidLoginCredentialsException

        # attempt to login the user 
        user = user_service.user_login(session, data['email'], data['password'])

        # create access token
        access_token = create_access_token(identity=user.user_id)

        session.commit() 

        serailized_user = serialize_user(user)

        return jsonify({ "token": access_token, "user": serailized_user }), 200

    except UserDoesNotExistException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400

    except InvalidLoginCredentialsException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400

    except Exception as e: 
        session.rollback()
        return jsonify({ "message": f"Server of Database error: {e}" }), 500 
    
    finally:
        session.close()

@auth_bp.route('/password/reset', methods=['POST'])
def reset_password():
    try:
        data = request.json 
        session = Session() 

        # Get the user email 
        email = data.get('email')
        if email is None: 
            raise MissingInformationException('Email') 
        
        # Get the user from the user email 
        user = user_service.get_user_info_by_email(session, data.get('email'))
        if user is None:
            raise UserDoesNotExistException
        
        # Create a token
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(data.get('email'), salt='password-reset')

        # Send email to user with token 
        send_reset_password_email(data.get('email'), token, mail)

        user_reset_password = auth_service.get_reset_password_by_email(session, email)
        if user_reset_password is None: 
            # Add the request to the table with a hashed token 
            auth_service.create_reset_password(session=session, token=hash_string(token), email=email)
        else: 
            auth_service.update_reset_password(session, email=email, token=hash_string(token))

        session.commit() 

        return jsonify({ "message": "Successfully sent reset password email", "email": email }), 200 
    
    except MissingInformationException as e: 
        session.rollback()
        return jsonify({ "message": str(e) }), 400 
    
    except Exception as e: 
        return jsonify({ 'message': f"Server or database error: {e}" }), 500 

    finally:
        session.close() 
    
@auth_bp.route('/password/create-new', methods=['POST'])
def create_new_password():
    try: 
        data = request.json
        session = Session() 

        user_email = data.get('email')
        if user_email is None: 
            raise MissingInformationException('Email')
        
        # Get the reset_token from the request and check if it exists 
        verification_token = data.get('verification_token')
        if verification_token is None: 
            raise MissingInformationException('verification_token')
        
        # Get the password_reset information and check if it exists
        reset_password = auth_service.get_reset_password_by_email(session=session, email=user_email)
        if reset_password is None: 
            raise MissingInformationException

        if not check_hashed_string(data.get('verification_token'), reset_password.token): 
            raise InvalidTokenException
        
        # Check if user is in database 
        user = user_service.get_user_info_by_email(session=session, email=user_email)
        if user is None: 
            raise UserDoesNotExistException
        
        # Get the new password that the user inputted from the request 
        new_password = data.get('password')
        new_password_confirmed = data.get('confirm_password')

        # Check if the password is given in the request 
        if new_password is None: 
            raise MissingInformationException('password')
        if new_password_confirmed is None: 
            raise MissingInformationException('confirmed password')
        
        # Check if the password is a valid password (meets requirements)
        if is_valid_password(data.get('confirm_password')) is False: 
            raise InvalidPasswordException("Password does meet requirements")
        
        # hash the password and then update the user's password 
        hashed_pass = hash_password(data.get('confirm_password'))
        user_service.update_password(session, user_email, hashed_pass)

        auth_service.delete_reset_password(session, user_email)

        session.commit() 
        
        return jsonify({ "message": "Password Successfully Reset" }), 200

    except UserDoesNotExistException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400
    
    except MissingInformationException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400
    
    except InvalidTokenException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400
    
    except Exception as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 500 

    finally: 
        session.close() 
        
        
        
