from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_bcrypt import Bcrypt

from flask_ckeditor import CKEditor






app = Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


from app.models import Blog
@login_manager.user_loader
def load_user(blog_id):
    return Blog.query.get(int(blog_id))



from app.models import Blog, Post, Subject, Comment # Importing to avoid circular import
from app.routes import main_routes, auth_routes, blog_routes
app.register_blueprint(main_routes)
app.register_blueprint(auth_routes,url_prefix='/auth')
app.register_blueprint(blog_routes,url_prefix='/blog')









'''
url_prefix='/auth'
'''