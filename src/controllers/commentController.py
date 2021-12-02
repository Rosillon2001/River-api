from database import db
from helpers.jwtTools import authTokenRequired, decodeToken 
from models.comment import Comment
from models.user import User

def getPostComments(id):
    try:
        # QUERY POST COMMENTS
        comments = Comment.query.filter_by(postID = id).order_by(Comment.id.asc()).all()

        # BUILD COMMENT LIST
        commentList = []
        for comment in comments:
            commentData = {'id': comment.id, 'userID': comment.userID, 'postID': comment.postID, 'content': comment.content, 'dateCreated': comment.dateCreated, 'username':comment.user.username, 'picture':comment.user.picture}
            commentList.append(commentData)

        return {'status': 200, 'comments': commentList}, 200
    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not get comments'}, 500

@authTokenRequired
def createComment(request, id):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        newComment = Comment(user.id, id, request.json['content'])
        db.session.add(newComment)
        db.session.commit()

        return {'status': 200, 'message': 'Comment created'}, 200
    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not create comment'}, 500

@authTokenRequired
def deleteComment(request, id):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # QUERY COMMENT AND CHECK IF EXISTS
        comment = Comment.query.get(id)
        if comment is None:
            return {'status': 404, 'message': 'Comment does not exist'}, 404

        if comment.userID == user.id:
            db.session.delete(comment)
            db.session.commit()
            return {'status': 200, 'message': 'Comment deleted'}, 200
        else:
            return {'status': 403, 'message': 'You cannot delete this comment'}, 403

    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not delete comment'}, 500