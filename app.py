from flask import Flask


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:password123@localhost:8889/blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
