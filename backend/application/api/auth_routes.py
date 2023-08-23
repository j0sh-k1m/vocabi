from flask import Blueprint, request, jsonify
from application import Session
from application.models.models import User
from application.utils.custom_exceptions import UserAlreadyExistsException, InvalidEmailException, InvalidPasswordException, UserDoesNotExistException, UrlParamDoesNotExistException
from application.utils.utils import hash_password
from application.utils.utils import is_valid_email, is_valid_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    from application.api import unverified_user_service

    try:
        print("Signing up...")
        data = request.json

        session = Session()

        if not is_valid_email(data['email']):
            raise InvalidEmailException(data['email'])

        if not is_valid_password(data['password']):
            raise InvalidPasswordException

        print("Valid email & password")

        hashed_password = hash_password(data['password'])
        unverified_user_service.create_user(
                    session, data['first_name'], data['last_name'], data['email'], hashed_password)  
          
        print("User created in unverified_user table")

        # Commit changes to db 
        session.commit()

        # TODO: Send verification email to user

        # Return a result message 
        return jsonify({ "message": f"Successfully created user: {data['email']} " }), 200
    
    except UserAlreadyExistsException as e:
        return jsonify({ "message": str(e) }), 400
    
    except InvalidEmailException as e:
        return jsonify({ "message": str(e) }), 400
    
    except InvalidPasswordException as e:
        return jsonify({ "message": str(e) }), 400
    
    except Exception as e: 
        # Handle exceptions 
        session.rollback() # Rollback (remove) changes 
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close() 

@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    from application.api import unverified_user_service, user_service

    try: 
        # url param <token>
        # token = request.args.get('token')
        print("Verifying email...")

        session = Session()

        # verify the user
        user = unverified_user_service.verify_user_token(session, token)
        print("Verified user:", user)

        # create user in user table 
        user_service.create_user(session, user.first_name, user.last_name, user.email, user.password)
        print("User created in user table")

        # delete user from unverified_user table 
        unverified_user_service.delete_user(session, user.user_id)

        session.commit()

        return jsonify({ "message": f"Successfully verified {user.email}" }), 200 

    # handle errors 
    except UserDoesNotExistException as e:
        return jsonify({ "message": str(e) }), 400
    
    except UserAlreadyExistsException as e:
        return jsonify({ "message": str(e) }), 400 
    
    except InvalidEmailException as e:
        return jsonify({ "message": str(e) }), 400 
    
    except InvalidPasswordException as e: 
        return jsonify({ "message": str(e) }), 400 
    
    except Exception as e:
        session.rollback()
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    return jsonify({ "message": "Not Implemented" })

    