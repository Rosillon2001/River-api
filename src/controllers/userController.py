import bcrypt
from database import db
from models.user import User
from models.follow import Follow
from models.post import Post, Repost
from helpers.jwtTools import authTokenRequired, decodeToken, generateToken
from helpers.fileUpload import saveImage, deleteImage
from operator import itemgetter


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
        elif('Key (email)' in e.args[0]):
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

        # GATHER FOLLOWS AND FOLLOWERS
        follows = []        # LIST OF IDs
        followingUsers = [] # LIST OF USER OBJECTS
        for follow in user.follows:
            follows.append(follow.followedID)
            followedUser = follow.followedUser
            followingUsers.append({'id': followedUser.id, 'username': followedUser.username, 'email': followedUser.email, 'name': followedUser.name, 'bio': followedUser.bio, 'location': followedUser.location, 'birthDate': followedUser.birthDate, 'picture': followedUser.picture, 'dateCreated': followedUser.dateCreated.strftime("%d/%m/%Y")})

        followers = []     # LIST OF IDs
        followerUsers = [] # LIST OF USER OBJECTS
        for follower in user.followers:
            followers.append(follower.followerID)
            followerUser = follower.followerUser
            followerUsers.append({'id': followerUser.id, 'username': followerUser.username, 'email': followerUser.email, 'name': followerUser.name, 'bio': followerUser.bio, 'location': followerUser.location, 'birthDate': followerUser.birthDate, 'picture': followerUser.picture, 'dateCreated': followerUser.dateCreated.strftime("%d/%m/%Y")})

        return {'status': 200, 'id': user.id, 'username': user.username, 'email': user.email, 'name': user.name, 'bio': user.bio, 'location': user.location, 'birthDate': user.birthDate, 'picture': user.picture, 'dateCreated': user.dateCreated.strftime("%d/%m/%Y"), 'follows': follows, 'followers': followers, 'postsNumber': len(user.posts.all()) + len(user.reposts.all()), 'followingUsers': followingUsers, 'followerUsers': followerUsers}, 200
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
            else:
                user.picture = saveImage('picture', 'static/images/profile/')
            changeFlag = True

        if changeFlag:
            db.session.commit()
            return {'status':200, 'message':'User updated successfully'}, 200
        else:
            return {'status':400, 'message':'Data provided is same as current'}, 400

    except Exception as e:
        print(e)
        if('Key (username)' in e.args[0]):
            return {'status': 409, 'message': 'Username already registered'}, 409
        elif('Key (email)' in e.args[0]):
            return {'status': 409, 'message': 'email already registered'}, 409
        else:
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


@authTokenRequired
def getUserByID(id):
    try:
        # QUERY REQUESTED USER
        requestedUser = User.query.get(id)
        
        if requestedUser is None:
            return {'status': 400, 'message': 'User does not exist'}, 400

        # GATHER FOLLOWS AND FOLLOWERS
        follows = []        # LIST OF IDs
        followingUsers = [] # LIST OF USER OBJECTS
        for follow in requestedUser.follows:
            follows.append(follow.followedID)
            followedUser = follow.followedUser
            followingUsers.append({'id': followedUser.id, 'username': followedUser.username, 'email': followedUser.email, 'name': followedUser.name, 'bio': followedUser.bio, 'location': followedUser.location, 'birthDate': followedUser.birthDate, 'picture': followedUser.picture, 'dateCreated': followedUser.dateCreated.strftime("%d/%m/%Y")})

        followers = []     # LIST OF IDs
        followerUsers = [] # LIST OF USER OBJECTS
        for follower in requestedUser.followers:
            followers.append(follower.followerID)
            followerUser = follower.followerUser
            followerUsers.append({'id': followerUser.id, 'username': followerUser.username, 'email': followerUser.email, 'name': followerUser.name, 'bio': followerUser.bio, 'location': followerUser.location, 'birthDate': followerUser.birthDate, 'picture': followerUser.picture, 'dateCreated': followerUser.dateCreated.strftime("%d/%m/%Y")})

        # GET USER POSTS
        posts = []
        for post in requestedUser.posts:
            reposters = [id[0] for id in post.reposts.with_entities(Repost.user_id).all()]
            postData = {'id': post.id, 'userID': post.user_id, 'username': post.user.username, 'name': post.user.name, 'picture': post.user.picture, 'likes': post.likes, 'text': post.text, 'images': post.images, 'dateCreated': post.dateCreated, 'repostNumber': len(reposters), 'reposters': reposters, 'type': 'post'}
            posts.append(postData)

        # GET USER REPOSTS
        reposts = []
        for repost in requestedUser.reposts:
            reposters = [id[0] for id in repost.post.reposts.with_entities(Repost.user_id).all()]
            repostData = {'id': repost.post.id, 'userID': repost.post.user_id, 'username': repost.post.user.username, 'name': repost.post.user.name, 'picture': repost.post.user.picture, 'likes': repost.post.likes, 'text': repost.post.text, 'images': repost.post.images, 'dateCreated': repost.dateCreated, 'postDateCreated': repost.post.dateCreated, 'repostNumber': len(reposters), 'reposters': reposters, 'type':'repost', 'reposterID': repost.user.id, 'reposterUsername': repost.user.username}
            reposts.append(repostData)      

        # COMBINE POSTS AND REPOSTS FOR SORTING BY DATE
        totalPosts = posts + reposts
        totalPosts.sort(key=itemgetter("dateCreated"))
        totalPosts.reverse()

        return {'status': 200, 'profile': {'id': requestedUser.id, 'username': requestedUser.username, 'email': requestedUser.email, 'name': requestedUser.name, 'bio': requestedUser.bio, 'location': requestedUser.location, 'birthDate': requestedUser.birthDate, 'picture': requestedUser.picture, 'dateCreated': requestedUser.dateCreated.strftime("%d/%m/%Y"), 'follows': follows, 'followers': followers, 'postsNumber': len(requestedUser.posts.all()) + len(requestedUser.reposts.all()), 'followingUsers': followingUsers, 'followerUsers': followerUsers}, 'posts': totalPosts }, 200
    except Exception as e:
        print(e)
        return {'status':500, 'message':"Could not get user"}, 500


@authTokenRequired
def followUser(request, id):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # QUERY REQUESTED USER AND CHECK IF EXISTS
        userToFollow = User.query.get(id)
        if userToFollow is None:
            return {'status': 400, 'message': 'User does not exist'}, 400
        elif user.id == userToFollow.id:
            return {'status': 400, 'message': 'You cannot follow yourself'}, 400

        # USER FOLLOWS (LIST OF IDS)
        followsIDs = []
        for follow in user.follows:
            followsIDs.append(follow.followedID)

        # CHECK IF THE USER IS ALREADY FOLLOWING THE REQUESTED USER 
        if int(id) in followsIDs:
            Follow.query.filter(Follow.followerID == userID, Follow.followedID == int(id)).delete()
            db.session.commit()
            return {'status': 200, 'message': 'User unfollowed'}, 200
        else:
            newFollow = Follow(user.id, id)
            db.session.add(newFollow)
            db.session.commit()
            return {'status': 200, 'message': 'User followed'}, 200

    except Exception as e:
        print(e)
        return {'status':500, 'message':"Could not process operation"}, 500