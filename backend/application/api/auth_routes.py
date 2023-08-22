from application import Session
from application.api import auth_bp 
from flask import request, jsonify 
from application.models.models import User

@auth_bp.route('/signup', methods=['POST'])
def user_signup():
    data = request.json 

    # data validation 
    required = ['email', 'first_name', 'last_name', 'password']

    for field in required: 
        if field not in data: 
            return jsonify({ "error": f"Missing required field: {field}" }), 400 

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    session = Session() 
    try: 
        existing_user = session.query(User).filter_by(email = email).first()
        if existing_user:
            return jsonify({ "error": "user with this email already exists" })
        
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        session.add(new_user)
        session.commit()
        return jsonify({ "message": "User successfully created" }), 201 

    except Exception as e:
        session.rollback()
        return jsonify({ "error": str(e) }), 500 