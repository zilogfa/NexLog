from flask import render_template, redirect, url_for, request, g
from flask import Blueprint
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_routes
from app.models import Blog, Post, Subject, Comment
# from app import db
# from app.models import Blog, Post, Comment, Subject

main_routes = Blueprint('main', __name__)

# -------- Globally to all render_templates ---------------------------------------
@main_routes.before_request
def before_request():
    """universally accessible without repeatedly passing them manually to every render_template call."""
    g.csrf_token = generate_csrf()  # from flask import g
#.....................................................................................



TITLE = "NexLog"

@main_routes.route('/')
def main():
    top_blogs = Blog.query.order_by(Blog.impressions.desc()).limit(3).all()
    top_posts = Post.query.order_by(Post.views.desc()).limit(3).all()
    return render_template('main/main.html', title=TITLE, top_posts=top_posts, top_blogs=top_blogs)


@main_routes.route('/about')
def about():
    return render_template('main/about.html', title=TITLE)