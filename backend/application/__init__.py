from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_socketio import SocketIO

db = SQLAlchemy()
Session = sessionmaker()
socketio = SocketIO() 

# TODO: Create app using Config
def create_application(dev_mode: str):
    app = Flask(__name__, instance_relative_config=False)

    if dev_mode == 'DEV':
        app.config.from_object("config.DevConfig")
    elif dev_mode == 'PROD':
        app.config.from_object("config.ProdConfig")
    
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session.configure(bind=engine)
    socketio.init_app(app, cors_allowed_origins="*")

    with app.app_context(): 

        from application.models.models import Base

        Base.metadata.create_all(engine, checkfirst=True)
        
        return app 
