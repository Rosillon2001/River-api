from database import db
from datetime import datetime, timedelta


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    likes = db.Column(db.ARRAY(db.Integer), default={})
    text = db.Column(db.String(200), nullable=False)
    images = db.Column(db.ARRAY(db.String(255)), nullable=True)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))
    reposts = db.relationship('Repost', cascade="all, delete", backref="post")
    comments = db.relationship('Comment', cascade="all, delete", backref="post")

    #CONSTRUCTOR
    def __init__(self, user_id, text, images):
        self.user_id = user_id
        self.text = text
        self.images = images

class Repost(db.Model):
    __tablename__ = 'reposts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))

    #CONSTRUCTOR
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id