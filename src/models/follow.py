from database import db
from sqlalchemy.sql import func

class Follow(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    followerID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followedID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dateCreated = db.Column(db.DateTime, default=func.now())

    #CONSTRUCTOR
    def __init__(self, followerID, followedID):
        self.followerID = followerID
        self.followedID = followedID