from flask_cors import CORS
from application import create_application, socketio 
from flask_jwt_extended import JWTManager

application = create_application("DEV")

CORS(application, origins=application.config['CORS_ALLOWED_ORIGINS'])

jwt = JWTManager(application)

def get_secret() -> str:
    return application.config['SECRET_KEY']

if __name__ == '__main__':
    socketio.run(application, port=6000, debug=True)