from database import db
from models.post import Post, Repost
from models.user import User
from helpers.jwtTools import authTokenRequired, decodeToken 
from helpers.fileUpload import deleteImage, saveImages
from operator import itemgetter


def getAllPosts():
    try:
        # QUERY POSTS AND REPOSTS
        posts = Post.query.all()
        reposts = Repost.query.all()

        # POST LIST
        postList = []
        for post in posts:
            reposters = [id[0] for id in post.reposts.with_entities(Repost.user_id).all()]
            postData = {'id': post.id, 'userID': post.user_id, 'username': post.user.username, 'name': post.user.name, 'picture': post.user.picture, 'likes': post.likes, 'text': post.text, 'images': post.images, 'dateCreated': post.dateCreated, 'repostNumber': len(reposters), 'reposters': reposters, 'type': 'post'}
            postList.append(postData)

        # REPOST LIST
        repostList = []
        for repost in reposts:
            reposters = [id[0] for id in repost.post.reposts.with_entities(Repost.user_id).all()]
            repostData = {'id': repost.post.id, 'userID': repost.post.user_id, 'username': repost.post.user.username, 'name': repost.post.user.name, 'picture': repost.post.user.picture, 'likes': repost.post.likes, 'text': repost.post.text, 'images': repost.post.images, 'dateCreated': repost.dateCreated, 'postDateCreated': repost.post.dateCreated, 'repostNumber': len(reposters), 'type':'repost', 'reposters': reposters, 'reposterID': repost.user.id, 'reposterUsername': repost.user.username}
            repostList.append(repostData)

        # COMBINE POSTS AND REPOSTS FOR SORTING BY DATE AND ID
        totalPosts = postList + repostList
        totalPosts.sort(key=itemgetter("dateCreated", "id"))
        totalPosts.reverse()

        return {'status': 200, 'totalPosts': totalPosts}, 200
    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not get posts'}, 500

@authTokenRequired
def getFeedPosts(request):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        totalPosts = []
        # GET FOLLOWED USER POSTS AND REPOSTS
        for follow in user.follows:
            posts = follow.followedUser.posts.all()
            reposts = follow.followedUser.reposts.all()
            # POSTS
            for post in posts:
                reposters = [id[0] for id in post.reposts.with_entities(Repost.user_id).all()]
                postData = {'id': post.id, 'userID': post.user_id, 'username': post.user.username, 'name': post.user.name, 'picture': post.user.picture, 'likes': post.likes, 'text': post.text, 'images': post.images, 'dateCreated': post.dateCreated, 'repostNumber': len(reposters), 'reposters': reposters, 'type': 'post'}
                totalPosts.append(postData)
            # REPOSTS
            for repost in reposts:
                reposters = [id[0] for id in repost.post.reposts.with_entities(Repost.user_id).all()]
                repostData = {'id': repost.post.id, 'userID': repost.post.user_id, 'username': repost.post.user.username, 'name': repost.post.user.name, 'picture': repost.post.user.picture, 'likes': repost.post.likes, 'text': repost.post.text, 'images': repost.post.images, 'dateCreated': repost.dateCreated, 'postDateCreated': repost.post.dateCreated, 'repostNumber': len(reposters), 'type':'repost', 'reposters': reposters, 'reposterID': repost.user.id, 'reposterUsername': repost.user.username}
                totalPosts.append(repostData)
        
        # GET USER'S POSTS AND REPOSTS
        # POSTS
        for post in user.posts:
            reposters = [id[0] for id in post.reposts.with_entities(Repost.user_id).all()]
            postData = {'id': post.id, 'userID': post.user_id, 'username': post.user.username, 'name': post.user.name, 'picture': post.user.picture, 'likes': post.likes, 'text': post.text, 'images': post.images, 'dateCreated': post.dateCreated, 'repostNumber': len(reposters), 'reposters': reposters, 'type': 'post'}
            totalPosts.append(postData)
        # REPOSTS
        for repost in user.reposts:
            reposters = [id[0] for id in repost.post.reposts.with_entities(Repost.user_id).all()]
            repostData = {'id': repost.post.id, 'userID': repost.post.user_id, 'username': repost.post.user.username, 'name': repost.post.user.name, 'picture': repost.post.user.picture, 'likes': repost.post.likes, 'text': repost.post.text, 'images': repost.post.images, 'dateCreated': repost.dateCreated, 'postDateCreated': repost.post.dateCreated, 'repostNumber': len(reposters), 'reposters': reposters, 'type':'repost', 'reposterID': repost.user.id, 'reposterUsername': repost.user.username}
            totalPosts.append(repostData)

        # SORT TOTAL POSTS BY DATE AND REVERSE THEM
        totalPosts.sort(key=itemgetter("dateCreated"))
        totalPosts.reverse()

        return {'status': 200, 'totalPosts': totalPosts}, 200
    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not get posts'}, 500

@authTokenRequired
def getUserPosts(request):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # GET USER POSTS
        posts = []
        for post in user.posts:
            reposters = [id[0] for id in post.reposts.with_entities(Repost.user_id).all()]
            postData = {'id': post.id, 'userID': post.user_id, 'username': post.user.username, 'name': post.user.name, 'picture': post.user.picture, 'likes': post.likes, 'text': post.text, 'images': post.images, 'dateCreated': post.dateCreated, 'repostNumber': len(reposters), 'reposters': reposters, 'type': 'post'}
            posts.append(postData)

        # GET USER REPOSTS
        reposts = []
        for repost in user.reposts:
            reposters = [id[0] for id in repost.post.reposts.with_entities(Repost.user_id).all()]
            repostData = {'id': repost.post.id, 'userID': repost.post.user_id, 'username': repost.post.user.username, 'name': repost.post.user.name, 'picture': repost.post.user.picture, 'likes': repost.post.likes, 'text': repost.post.text, 'images': repost.post.images, 'dateCreated': repost.dateCreated, 'postDateCreated': repost.post.dateCreated, 'repostNumber': len(reposters), 'reposters': reposters, 'type':'repost', 'reposterID': repost.user.id, 'reposterUsername': repost.user.username}
            reposts.append(repostData)

        # COMBINE POSTS AND REPOSTS FOR SORTING BY DATE
        totalPosts = posts + reposts
        totalPosts.sort(key=itemgetter("dateCreated"))
        totalPosts.reverse()

        return {'status': 200, 'totalPosts': totalPosts}, 200
    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not get posts'}, 500

@authTokenRequired
def createPost(request):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        if user is None:
            return {'status': 400, 'message': 'Cannot post if you are not logged in'}, 400

        content = request.form['postText']
        pictures = None
        if('images' in request.files and request.files['images'].filename != ""):
            pictures = saveImages('images', 'static/images/posts/')

        newPost = Post(user.id, content, pictures)
        db.session.add(newPost)
        db.session.commit()

        return {'status':200, 'message':'Post successfully created'}, 200

    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not post'}, 500

@authTokenRequired
def deletePost(postID):
    try: 
        post = Post.query.get(postID)

        if post is None:
            return {'status':400, 'message':'No post to delete, does not exist'}, 400

        if post.images:
            for image in post.images:
                deleteImage(image)

        db.session.delete(post)
        db.session.commit()

        return {'status':200, 'message':'Post successfully deleted'}, 200

    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not delete post'}, 500

@authTokenRequired
def repost(request, id):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # QUERY POST AND CHECK IF POST EXISTS
        post = Post.query.get(id)
        if post is None:
            return {'status':400, 'message':'Post does not exist'}, 400
        
        # CHECK IF USER IS THE OWNER OF THE POST
        postIds = [id[0] for id in user.posts.with_entities(Post.id).all()]
        if int(id) in postIds:
            return {'status':400, 'message':'Cannot repost your own post'}, 400

        # GET USER'S REPOSTS (IDs)
        repostIds = [id[0] for id in user.reposts.with_entities(Repost.post_id).all()]
        # IF POST ID IN USER REPOSTS IDs THEN REMOVE REPOST
        if int(id) in repostIds:
            repost = Repost.query.filter(Repost.user_id == user.id, Repost.post_id == post.id).first()
            db.session.delete(repost)
            db.session.commit()
            return {'status':200, 'message':'Removed repost'}, 200
        # IF POST ID NOT IN USER REPOSTS IDs THEN CREATE REPOST
        else:
            newRepost = Repost(user.id, post.id)
            db.session.add(newRepost)
            db.session.commit()
            return {'status':200, 'message':'Successfully reposted'}, 200

    except Exception as e:
        print(e)
        return {'status':500, 'message':'An error occurred'}, 500

@authTokenRequired
def likePost(request, id):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # QUERY POST AND CHECK IF EXISTS
        post = Post.query.get(id)
        if post is None:
            return {'status':400, 'message':'Post does not exist'}, 400

        # OBTAIN POST LIKES ARRAY AND CHECK IF USER'S ID IS IN THE ARRAY FOR LIKING OR REMOVING LIKE
        postLikes = post.likes.copy()
        if int(user.id) in postLikes:
            postLikes.remove(user.id)
            post.likes = postLikes
            db.session.commit()
            return {'status': 200, 'message': 'Removed like'}, 200
        else:
            postLikes.append(user.id)
            post.likes = postLikes
            db.session.commit()
            return {'status': 200, 'message': 'Post liked'}, 200

    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'An error occurred'}, 500