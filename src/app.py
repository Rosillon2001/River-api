from flask import Flask
from flask_cors import CORS
from database import db
from cloudinary import config

from dotenv import load_dotenv
load_dotenv()

from config import *

from routes.user import user_bp
from routes.post import post_bp
from routes.search import search_bp
from routes.comment import comment_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(search_bp)
app.register_blueprint(comment_bp)

#Cloudinary config
config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('CLOUDINARY_KEY'), 
    api_secret=os.getenv('CLOUDINARY_SECRET'))

@app.route("/")
def index():
    return "River social media API"

if __name__ == '__main__':
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run()