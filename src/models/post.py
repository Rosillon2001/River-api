from database import db
from datetime import datetime, timedelta


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    likes = db.Column(db.ARRAY(db.Integer), nullable=True)
    text = db.Column(db.String(200), nullable=False)
    images = db.Column(db.ARRAY(db.String(255)), nullable=True)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow()-timedelta(hours=4))

    #CONSTRUCTOR
    def __init__(self, user_id, likes, text, images):
        self.user_id = user_id
        self.likes = likes
        self.text = text
        self.images = images

