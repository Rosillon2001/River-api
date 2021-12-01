from sqlalchemy.orm import backref
from database import db
from datetime import datetime, timedelta


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(65), nullable=False)
    name = db.Column(db.String(60), nullable=True)
    bio = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(60), nullable=True)
    birthDate = db.Column(db.String(10), nullable=True)
    picture = db.Column(db.String(255), nullable=True, default=None)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))
    posts = db.relationship('Post', cascade="all, delete", backref="user")
    reposts = db.relationship('Repost', cascade="all, delete", backref="user")

    # CONSTRUCTOR
    def __init__(self, username, email, password, name, bio, location, birthDate, picture):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.bio = bio
        self.location =  location
        self.birthDate = birthDate
        self.picture = picture