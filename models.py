from app import db, app
from hashutils import make_pw_hash
from flask_migrate import Migrate

from datetime import date, time, datetime
from flask_login import UserMixin

migrate = Migrate(app, db)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    pw_hash = db.Column(db.String(120))
    # SQLAlchemy will load the data as necessary in one go
    posts = db.relationship('Post', backref='owner')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.pw_hash = make_pw_hash(password)


class Post(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    post_title = db.Column(db.String(120), nullable=False)
    post_body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, post_title, post_body, owner):
        self.post_title = post_title
        self.post_body = post_body
        self.owner = owner
