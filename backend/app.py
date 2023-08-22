from flask_cors import CORS
from application import create_application, socketio 

application = create_application("DEV")

CORS(application)

if __name__ == '__main__':
    socketio.run(application, port=5000, debug=True)