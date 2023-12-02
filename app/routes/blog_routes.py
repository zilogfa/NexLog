from flask import render_template, redirect, url_for, request, abort, g
from flask import Blueprint
from flask_login import login_required, current_user

from flask_wtf.csrf import generate_csrf
from app import db
from app.models import Blog, Post, Subject, Comment
from app.forms.comment_forms import CommentForm
from . import auth_routes


blog_routes = Blueprint('blog', __name__, subdomain='<user_subdomain>')

# -------- Globally to all render_templates ---------------------------------------
@blog_routes.before_request
def before_request():
    """universally accessible without repeatedly passing them manually to every render_template call."""
    g.csrf_token = generate_csrf()  # from flask import g
#.....................................................................................


def get_subjects_for_blog(blog_id):
    subjects = Subject.query \
        .join(Post.subjects) \
        .filter(Post.blog_id == blog_id) \
        .distinct().all()
    return subjects


@blog_routes.route('/')
def blog(user_subdomain):
    blog = Blog.query.filter_by(subdomain=user_subdomain).first()
    posts = Post.query.filter_by(blog_id=blog.id).order_by(Post.created_at.desc()).all()
    subjects = get_subjects_for_blog(blog.id)
    top_posts = Post.query.filter_by(blog_id=blog.id).order_by(Post.views.desc()).limit(5).all()

    blog.impressions += 1
    db.session.commit()
    
    return render_template('blog.html', posts=posts, blog=blog, subjects=subjects, top_posts=top_posts, subdomain=user_subdomain)


@blog_routes.route('/view_post/<int:post_id>', methods=['GET', 'POST'])
def view_post(user_subdomain, post_id):
    form = CommentForm()
    blog = Blog.query.filter_by(subdomain=user_subdomain).first()
    if not blog:
        abort(404, description="Blog not found")

    post = Post.query.filter_by(id=post_id, blog_id=blog.id).first()
    if not post:
        abort(404, description="Post not found")

    if form.validate_on_submit():
        new_comment = Comment(
            post_id= post.id,
            blog_id= blog.id,
            name= form.name.data,
            body = form.body.data
        )
        db.session.add(new_comment)
        db.session.commit()
        print(f'New comment added; Blod ID:{blog.id}; Post ID:{post.id}')
        return redirect(url_for('blog.view_post', post_id=post.id, user_subdomain=user_subdomain))
    else:
        print(form.errors)
    comments = Comment.query.filter_by(post_id=post_id, blog_id=blog.id).all()  
    subjects = get_subjects_for_blog(blog.id)
    top_posts = Post.query.filter_by(blog_id=blog.id).order_by(Post.views.desc()).limit(5).all()
    blog.impressions += 1
    post.views += 1
    db.session.commit()
    return render_template('view_post.html', post=post, blog=blog, subjects=subjects, top_posts=top_posts, form=form, subdomain=user_subdomain, comments=comments)



@blog_routes.route('/subject/<int:subject_id>/posts')
def posts_by_subject(user_subdomain, subject_id):
    blog = Blog.query.filter_by(subdomain=user_subdomain).first()
    if not blog:
        abort(404, description="Blog not found")

    subject = Subject.query.filter_by(id=subject_id).first()
    if not subject:
        abort(404, description="Subject not found")

    posts = Post.query.join(Post.subjects).filter(Subject.id == subject_id, Post.blog_id == blog.id).all()
    all_subjects = get_subjects_for_blog(blog.id)
    top_posts = Post.query.filter_by(blog_id=blog.id).order_by(Post.views.desc()).limit(5).all()
    blog.impressions += 1
    db.session.commit()
    return render_template('posts_by_subject.html', posts=posts, subject=subject, subjects=all_subjects,top_posts=top_posts, blog=blog, subdomain=user_subdomain)



# Top Posts from all posts.
# top_posts = Post.query.order_by(Post.views.desc()).limit(5).all()