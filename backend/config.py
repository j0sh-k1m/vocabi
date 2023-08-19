import secrets
import os
from dotenv import load_dotenv
load_dotenv()

class Config: 
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = secrets.token_hex(16)

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TACK_MODIFICATIONS = False 

    PROPAGATE_EXCEPTIONS = True 

    # TODO: Implement Logging
    # LOGGING_LEVEL = "INFO"
    # LOGGING_LOCATION = "logs/app.log"
    

class DevConfig(Config):
    DEBUG = True 
    TEMPLATES_AUTO_RELOAD = True 

    # NOTE: "*" gives access to API from all domains (Security Risk)
    CORS_ALLOWED_ORIGINS = ["*"]

class ProdConfig(Config):
    DEBUG = False 
    TEMPLATES_AUTO_RELOAD = False 

    PROPAGATE_EXCEPTIONS = False 

    # TODO: Set the paths that can access API
    CORS_ALLOWED_ORIGINS = ['']

    # TODO: Implement Logging
    # LOGGING_LEVEL = "WARNING"
    # LOGGING_LOCATION = "logs/app.log"
