from flask import Blueprint, request
from controllers.userController import registerUser, loginUser, getUser, updateUser, deleteUser, getUserByID, followUser

user_bp = Blueprint('user_bp', __name__)


@user_bp.route("/register", methods=['POST'])
def register():
    if(request.method == 'POST'):
        return registerUser(request)


@user_bp.route('/login', methods=['POST'])
def login():
    if(request.method == 'POST'):
        return loginUser(request)

@user_bp.route('/user', methods=['GET', 'PUT', 'DELETE'])
def user():
    if(request.method == 'GET'):
        return getUser(request)
    if(request.method == 'PUT'):
        return updateUser(request)
    if(request.method == 'DELETE'):
        return deleteUser(request)

@user_bp.route('/user/<id>', methods=['GET'])
def userID(id):
    if(request.method == 'GET'):
        return getUserByID(id)

@user_bp.route('/follow/<id>', methods=['POST'])
def followID(id):
    if(request.method == 'POST'):
        return followUser(request, id)