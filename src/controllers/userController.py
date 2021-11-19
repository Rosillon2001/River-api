import bcrypt
from database import db
from models.user import User
from helpers.jwtTools import authTokenRequired, decodeToken, generateToken
from helpers.fileUpload import saveImage, deleteImage


def registerUser(request):
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode()

        name = bio = location = birthDate = picture = None

        if(request.form['name'] != ""):
            name = request.form['name']
        if(request.form['bio'] != ""):
            bio = request.form['bio']
        if(request.form['location'] != ""):
            location = request.form['location']
        if(request.form['birthDate'] != ""):
            birthDate = request.form['birthDate']
        if('picture' in request.files and request.files['picture'].filename != ""):
            picture = saveImage('picture', 'static/images/profile/')

        newUser = User(username, email, hashedPassword, name, bio, location, birthDate, picture)
        db.session.add(newUser)
        db.session.commit()

        return {'status': 200, 'message': 'User created successfully.'}, 200
    except Exception as e:
        if('Key (username)' in e.args[0]):
            return {'status': 409, 'message': 'Username already registered'}, 409
        elif('key (email)' in e.args[0]):
            return {'status': 409, 'message': 'email already registered'}, 409
        else:
            return {'status': 500, 'message': 'Could not process register'}, 500
            

def loginUser(request):
    try:
        user = User.query.filter((User.username == request.json['user']) | (User.email == request.json['user'])).first()
        
        if(user is not None):
            if bcrypt.checkpw(request.json['password'].encode('utf-8'), user.password.encode('utf-8')):
                userToken = generateToken({'id':user.id, 'user':user.username, 'email':user.email})
                return {'status': 200, 'message': 'Login successful', 'token': userToken}, 200
            else:
                return {'status': 401, 'message': 'Invalid credentials'}, 401
        else:
            return {'status': 401, 'message': 'User not registered'}, 401

    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not process login'}, 500


@authTokenRequired
def getUser(request):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        if user is None:
            return {'status': 400, 'message': 'User does not exist'}, 400

        return {'status': 200, 'id': user.id, 'username': user.username, 'email': user.email, 'name': user.name, 'bio': user.bio, 'location': user.location, 'birthDate': user.birthDate, 'picture': user.picture, 'dateCreated': user.dateCreated.strftime("%d/%m/%Y")}, 200
    except Exception as e:
        print(e)
        return {'status': 500, 'message':'Could not get user data'}, 500


@authTokenRequired
def updateUser(request):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        if(user is None):
            return {'status': 400, 'message': 'User does not exist'}, 400

        changeFlag = False
        if user.username != request.form['username']:
            user.username = request.form['username']
            changeFlag = True
        if user.email != request.form['email']:
            user.email = request.form['email']
            changeFlag = True
        if request.form['password'] != "":
            user.password = bcrypt.hashpw(request.form['password'].encode('utf8'), bcrypt.gensalt()).decode()
            changeFlag = True
        if request.form['name'] != user.name and request.form['name'] != "":
            user.name = request.form['name']
            changeFlag= True
        if request.form['bio'] != user.bio and request.form['bio'] != "":
            user.bio = request.form['bio']
            changeFlag= True
        if request.form['location'] != user.location and request.form['location'] != "":
            user.location = request.form['location']
            changeFlag= True
        if request.form['birthDate'] != user.birthDate and request.form['birthDate'] != "":
            user.birthDate = request.form['birthDate']
            changeFlag= True
        if('picture' in request.files and request.files['picture'].filename != ""):
            if user.picture:
                deleteImage(user.picture)
            user.picture = saveImage('picture', 'static/images/profile/')
            changeFlag = True

        if changeFlag:
            db.session.commit()
            return {'status':200, 'message':'User updated successfully'}, 200
        else:
            return {'status':400, 'message':'Data provided is same as current'}, 400

    except Exception as e:
        print(e)
        return {'status':500, 'message':"Could not update user"}, 500


@authTokenRequired
def deleteUser(request):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        if user is None:
            return {'status': 400, 'message': 'User does not exist'}, 400

        if user.picture:
            deleteImage(user.picture)

        db.session.delete(user)
        db.session.commit()
        return {'status':200, 'message':'User deleted successfully'}, 200
    except Exception as e:
        print(e)
        return {'status':500, 'message':"Could not delete user"}, 500