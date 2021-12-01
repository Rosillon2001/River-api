from flask import Blueprint, request
from controllers.postController import getUserPosts, createPost, deletePost

post_bp = Blueprint('post_bp', __name__)

@post_bp.route("/post", methods=['GET', 'POST'])
def post():
    if(request.method == 'GET'):
        return getUserPosts(request)
    if(request.method == 'POST'):
        return createPost(request)

@post_bp.route("/post/<id>", methods=['DELETE'])
def post_id(id):
    if(request.method == 'DELETE'):
        return deletePost(id)
