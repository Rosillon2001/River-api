from database import db
from models.post import Post
from models.user import User
from helpers.jwtTools import authTokenRequired, decodeToken 
from helpers.fileUpload import saveImage, deleteImage, saveImages

@authTokenRequired
def createPost(request):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)

        if user is None:
            return {'status': 400, 'message': 'Cannot post if you are not logged in'}, 400

        content = request.form['postText']
        if('images' in request.files and request.files['images'].filename != ""):
            picture = saveImages('images', 'static/images/posts/')

        likes = []

        newPost = Post(user.id,likes,content,picture)
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



