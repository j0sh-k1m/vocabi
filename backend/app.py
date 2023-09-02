from flask_cors import CORS
from application import create_application, socketio 
from flask_jwt_extended import JWTManager
from flask_mail import Mail 

application = create_application("DEV")

CORS(application, origins=application.config['CORS_ALLOWED_ORIGINS'])

jwt = JWTManager(application)
mail = Mail(application)

if __name__ == '__main__':
    socketio.run(application, port=8080, debug=True)