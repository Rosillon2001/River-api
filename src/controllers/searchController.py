from sqlalchemy import or_
from models.user import User
from models.post import Post

def searchKeyword(keyword):
    try:

        # GATHER USERS
        users = User.query.filter(or_(User.username.ilike("%"+keyword+"%"), User.name.ilike("%"+keyword+"%"), User.bio.ilike("%"+keyword+"%"))).order_by(User.id.desc()).all()
        userList = []
        for user in users:
            userData = {'id': user.id, 'username': user.username, 'email': user.email, 'name': user.name, 'bio': user.bio, 'location': user.location, 'birthDate': user.birthDate, 'picture': user.picture, 'dateCreated': user.dateCreated.strftime("%d/%m/%Y")}
            userList.append(userData)

        # GATHER POSTS
        posts = Post.query.filter(Post.text.ilike("%"+keyword+"%")).order_by(Post.id.desc()).all()
        postList = []
        for post in posts:
            postData = {'id': post.id, 'userID': post.user_id, 'username': post.user.username, 'name': post.user.name, 'picture': post.user.picture, 'likes': post.likes, 'text': post.text, 'images': post.images, 'dateCreated': post.dateCreated, 'repostNumber': len(post.reposts), 'type': 'post'}
            postList.append(postData)

        return {'status': 200, 'users': userList, 'posts': postList}, 200
    except Exception as e:
        print(e)
        return {'status': 500, 'message': 'Could not perform search'}, 500