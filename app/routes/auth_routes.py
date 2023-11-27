from flask import render_template, redirect, url_for, request, flash, jsonify, g
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_manager

from app import db, bcrypt
from app.models import Blog, Subject, Post, Comment
from app.forms.auth_forms import LoginForm, RegistrationForm
from app.forms.post_forms import PostForm, SubjectForm
from app.routes.blog_routes import blog_routes
from . import auth_routes

from flask_ckeditor import upload_success, upload_fail
from flask_wtf.csrf import generate_csrf
from datetime import datetime

import os
import secrets
from PIL import Image  # pip Pillow
from flask import current_app

auth_routes = Blueprint('auth', __name__)


# Login >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def save_post_picture(file):
    if not file:
        return None
    # Generating a secure random string as the filename
    random_hex = secrets.token_hex(8)
    # Getting the file extension
    _, file_extension = os.path.splitext(file.filename)
    # Creating a new filename using the random string and the original extension
    new_filename = random_hex + file_extension
    # Setting the destination folder to save the post pictures
    destination = os.path.join(
        current_app.root_path, 'static/images/post_pictures', new_filename)

    # Resize the image to a desired size (optional)
    output_size = (1200, 1200)  # Adjust the size as needed
    image = Image.open(file)
    image.thumbnail(output_size)

    # Saving the resized image to the destination folder
    image.save(destination)

    # Returning the filename to store in the database
    return new_filename


# -------- Globally to all render_templates ---------------------------------------
@auth_routes.before_request
def before_request():
    """universally accessible without repeatedly passing them manually to every render_template call."""
    g.csrf_token = generate_csrf()  # from flask import g

# Login >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------


@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        blog = Blog.query.filter_by(email=(form.email.data).lower()).first()
        if blog and blog.verify_password(form.password.data):
            login_user(blog, remember=form.remember.data)
            return redirect(url_for('auth.admin_dashboard'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('auth/login.html', title='Login', form=form, logged_in=current_user.is_authenticated)


# Register >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("\n**Registeration for is Validate\n")
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        blog = Blog(
            email=(form.email.data).lower(),
            password=hashed_password,
            subdomain=(form.subdomain.data).lower(),
            blog_title=form.blog_title.data,
            blog_subtitle=form.blog_subtitle.data,
            author=form.author.data
        )
        # blog.set_password(form.password.data, bcrypt)
        db.session.add(blog)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))
    print("\n** Register Page")
    return render_template('auth/register.html', title='Register', form=form)

# LogOut >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------


@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.main'))


# Admin Dashboard >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------
@auth_routes.route('/admin_dashboard')
@login_required
def admin_dashboard():
    posts = Post.query.all()
    # if current_user.subdomain != user_subdomain:
    #     return redirect(url_for('main.index'))
    return render_template('auth/admin_dashboard.html', current_user=current_user, posts=posts)


# Create_subject >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------
@auth_routes.route('/create_subject', methods=['GET', 'POST'])
@login_required
def create_subject():
    form = SubjectForm()
    subjects = Subject.query.all()
    if form.validate_on_submit():
        print('form is valid')
        new_subject = Subject(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(new_subject)
        db.session.commit()
        print(f'New subject added: {form.name.data}')
        return redirect(url_for('auth.create_subject'))
    return render_template('auth/create_subject.html', current_user=current_user, form=form, subjects=subjects)

# Edit_subject >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------


@auth_routes.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = SubjectForm(obj=subject)
    if form.validate_on_submit():
        print('form is valid')

        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()

        print(f'subject updated: {form.name.data}')
        return redirect(url_for('auth.create_subject', subject_id=subject.id))
    return render_template('auth/edit_subject.html', current_user=current_user, form=form, subject=subject)

# DELETE_subject >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------


@auth_routes.route('/delete_subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.filter_by(id=subject_id).first()
    if subject:
        print('form is valid')
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Post not found'}), 404


# Create_Post >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------
@auth_routes.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    posts = Post.query.all()
    blog_id = current_user.id
    if form.validate_on_submit():
        print('form is valid')
        new_post = Post(
            blog_id=blog_id,
            title=form.title.data,
            subtitle=form.subtitle.data,
            post_pic=save_post_picture(
                form.post_pic.data) if form.post_pic.data else None,
            body=form.body.data
        )
        if form.subject.data:
            new_post.subjects.append(form.subject.data)
        db.session.add(new_post)
        db.session.commit()
        print(f'New post added: {form.title.data}')
        return redirect(url_for('auth.admin_dashboard'))
    return render_template('auth/create_post.html', current_user=current_user, form=form, posts=posts)

# DELETE_post >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------


@auth_routes.route('/delete_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def post_subject(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        print('form is valid')
        db.session.delete(post)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Post not found'}), 404




# SETTING Main Page >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------


@auth_routes.route('/setting')
@login_required
def setting():
    return render_template('auth/setting.html')