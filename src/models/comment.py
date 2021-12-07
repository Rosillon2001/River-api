from database import db
from sqlalchemy.sql import func

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    postID = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    dateCreated = db.Column(db.DateTime, default=func.now())

    #CONSTRUCTOR
    def __init__(self, userID, postID, content):
        self.userID = userID
        self.postID = postID
        self.content = content