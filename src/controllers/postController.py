from database import db
from models.post import Post
from models.user import User
from helpers.jwtTools import authTokenRequired, decodeToken 
from helpers.fileUpload import deleteImage, saveImages
from operator import itemgetter


@authTokenRequired
def getUserPosts(request):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        # GET USER POSTS
        posts = []
        for post in user.posts:
            postData = {'id': post.id, 'userID': post.user_id, 'username': post.user.username, 'name': post.user.name, 'picture': post.user.picture, 'likes': post.likes, 'text': post.text, 'images': post.images, 'dateCreated': post.dateCreated, 'repostNumber': len(post.reposts), 'type': 'post'}
            posts.append(postData)

        # GET USER REPOSTS
        reposts = []
        for repost in user.reposts:
            repostData = {'id': repost.post.id, 'userID': repost.post.user_id, 'username': repost.post.user.username, 'name': repost.post.user.name, 'picture': repost.post.user.picture, 'likes': repost.post.likes, 'text': repost.post.text, 'images': repost.post.images, 'dateCreated': repost.dateCreated, 'postDateCreated': repost.post.dateCreated, 'repostNumber': len(post.reposts), 'type':'repost'}
            reposts.append(repostData)

        # COMBINE POSTS AND REPOSTS FOR SORTING BY DATE
        totalPosts = posts + reposts
        totalPosts.sort(key=itemgetter("dateCreated"))

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

        return {'status':200, 'message':'Post successfully created'}

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

        return {'status':200, 'message':'Post successfully deleted'}

    except Exception as e:
        print(e)
        return {'status':500, 'message':'Could not delete post'}