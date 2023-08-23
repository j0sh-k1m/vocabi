from flask_cors import CORS
from application import create_application, socketio 
from config import DevConfig

application = create_application("DEV")

CORS(application, origins=application.config['CORS_ALLOWED_ORIGINS'])

def get_secret() -> str:
    return application.config['SECRET_KEY']

if __name__ == '__main__':
    socketio.run(application, port=6000, debug=True)