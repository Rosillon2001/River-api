from database import db
from sqlalchemy.sql import func


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
    dateCreated = db.Column(db.DateTime, default=func.now())
    posts = db.relationship('Post', cascade="all, delete", backref="user", lazy='dynamic')
    reposts = db.relationship('Repost', cascade="all, delete", backref="user", lazy='dynamic')
    comments = db.relationship('Comment', cascade="all, delete", backref="user")
    followers = db.relationship('Follow', foreign_keys='Follow.followedID', cascade="all, delete", backref="followedUser")
    follows = db.relationship('Follow', foreign_keys='Follow.followerID', cascade="all, delete", backref="followerUser")

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