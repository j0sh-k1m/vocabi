import os 
from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

db = SQLAlchemy(app)

if __name__ == 'main':
    app.run(debug=True)
