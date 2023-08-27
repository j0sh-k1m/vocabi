from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_socketio import SocketIO

db = SQLAlchemy()
Session = sessionmaker()
socketio = SocketIO() 

def create_application(dev_mode: str):
    app = Flask(__name__, instance_relative_config=False)

    if dev_mode == 'DEV':
        app.config.from_object("config.DevConfig")
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False 
    elif dev_mode == 'PROD':
        app.config.from_object("config.ProdConfig")
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = True 
    
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session.configure(bind=engine)
    socketio.init_app(app, cors_allowed_origins="*")

    with app.app_context(): 

        from application.models.models import Base
        from application.api.auth_routes import auth_bp
        from application.api.user_routes import user_bp
        from application.api.word_list_routes import word_list_bp

        # app.register_blueprint(users_bp) 
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(word_list_bp)

        # for rule in app.url_map.iter_rules():
        #     print(rule.endpoint, rule.methods, rule.rule)

        Base.metadata.create_all(engine, checkfirst=True)
        
        return app 
