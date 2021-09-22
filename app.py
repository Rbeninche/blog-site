from flask import Flask
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:password123@localhost:8889/blog'

SQLALCHEMY_DB_URL = os.getenv('DB_CONN')

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
