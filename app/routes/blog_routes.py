from flask import render_template, redirect, url_for, request
from flask import Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import Blog, Post, Subject
from . import auth_routes


blog_routes = Blueprint('blog', __name__, subdomain='<user_subdomain>')

@blog_routes.route('/')
def blog(user_subdomain):
    blog = Blog.query.filter_by(subdomain=user_subdomain).first()
    posts = Post.query.filter_by(blog_id=blog.id).order_by(Post.created_at.desc()).all()
    subjects = Subject.query.all()
    top_posts = Post.query.filter_by(blog_id=blog.id).order_by(Post.views.desc()).limit(5).all()
    
    return render_template('blog.html', posts=posts, blog=blog, subjects=subjects, top_posts=top_posts)

# @blog_routes.route('/admin_dashboard')
# @login_required
# def admin_dashboard():
#     # if current_user.subdomain != user_subdomain:
#     #     return redirect(url_for('main.index'))
#     return render_template('admin_dashboard.html')


# @blog_routes.route('/')
# def blog():
#     pass


@blog_routes.route('/view_post')
def view_post():
    pass





# Top Posts from all posts.
# top_posts = Post.query.order_by(Post.views.desc()).limit(5).all()