from flask import Flask
from dbconnect import connection_string


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:password123@localhost:8889/blog'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
