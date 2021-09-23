from flask import Flask
from dotenv import load_dotenv

import os

from flask_sqlalchemy import SQLAlchemy

load_dotenv()


app = Flask(__name__)
app.jinja_env.filters['zip'] = zip


app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:password123@localhost:8889/blog'


SQLALCHEMY_DB_URL = os.environ.get('JAWSDB_URL')

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
