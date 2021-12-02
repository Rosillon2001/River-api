from flask import Blueprint, request
from controllers.commentController import getPostComments, createComment, deleteComment

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route("/comments/<id>", methods=['GET', 'POST'])
def comments_id(id):
    if(request.method == 'GET'):
        return getPostComments(id)
    if(request.method == 'POST'):
        return createComment(request, id)

@comment_bp.route("/comment/<id>", methods=['DELETE'])
def comment_id(id):
    if(request.method == 'DELETE'):
        return deleteComment(request, id)