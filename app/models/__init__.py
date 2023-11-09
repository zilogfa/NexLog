from flask import Blueprint
models = Blueprint('models', __name__)

from .blog import Blog
from .post import Post
from .comment import Comment
from .subject import Subject
