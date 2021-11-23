from flask import Blueprint, request
from controllers.postController import createPost, deletePost

post_bp = Blueprint('post_bp', __name__)

@post_bp.route("/newPost", methods=['POST'])
def post():
    if(request.method == 'POST'):
        return createPost(request)

@post_bp.route("/deletePost/<ID>", methods=['DELETE'])
def delete(ID):
    if(request.method == 'DELETE'):
        return deletePost(ID)
