from flask import Blueprint, request
from controllers.userController import registerUser, loginUser, getUser, updateUser, deleteUser

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