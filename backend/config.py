import secrets
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class Config: 
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = secrets.token_hex(16)

    JWT_SECRET_KEY = secrets.token_hex(16)

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    PROPAGATE_EXCEPTIONS = True 

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465 
    MAIL_USE_TLS = False 
    MAIL_USE_SSL = True 
    MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")    

    # TODO: Implement Logging
    # LOGGING_LEVEL = "INFO"
    # LOGGING_LOCATION = "logs/app.log"
    

class DevConfig(Config):
    DEBUG = True 
    TEMPLATES_AUTO_RELOAD = True 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # NOTE: "*" gives access to API from all domains (Security Risk)
    CORS_ALLOWED_ORIGINS = ["*"]
    WEB_APPLICATION_ROOT = "http://localhost:5173" 
    SERVER_APPLICATION_ROOT = "http://127.0.0.1:8080"



class ProdConfig(Config):
    DEBUG = False 
    TEMPLATES_AUTO_RELOAD = False 

    PROPAGATE_EXCEPTIONS = False 

    # TODO: Set the paths that can access API
    CORS_ALLOWED_ORIGINS = ['']

    # TODO: Implement Logging
    # LOGGING_LEVEL = "WARNING"
    # LOGGING_LOCATION = "logs/app.log"
