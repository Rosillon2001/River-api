from flask import Blueprint, request
from controllers.postController import getAllPosts, getUserPosts, createPost, deletePost, repost, likePost, getFeedPosts

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

@post_bp.route("/posts", methods=['GET'])
def posts():
    if(request.method == 'GET'):
        return getAllPosts()

@post_bp.route("/feed", methods=['GET'])
def feed():
    if(request.method == 'GET'):
        return getFeedPosts(request)

@post_bp.route("/repost/<id>", methods=['POST'])
def repost_id(id):
    if(request.method == 'POST'):
        return repost(request, id)

@post_bp.route("/like/<id>", methods=['POST'])
def like_id(id):
    if(request.method == 'POST'):
        return likePost(request, id)