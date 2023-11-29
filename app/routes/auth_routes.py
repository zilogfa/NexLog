from flask import render_template, redirect, url_for, request, flash, jsonify, g
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_manager

from app import db, bcrypt
from app.models import Blog, Subject, Post, Comment
from app.forms.auth_forms import LoginForm, RegistrationForm, ProfileForm, ProfilePicForm, HeaderPicForm
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



# Save Pictures >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def save_post_picture(file):
    # Check if the file is a new file upload
    if hasattr(file, 'filename') and file.filename != '':
        # Generating a secure random string as the filename
        random_hex = secrets.token_hex(8)
        _, file_extension = os.path.splitext(file.filename)
        # Creating a new filename using the random string and the original extension
        new_filename = random_hex + file_extension
        # Setting the destination folder to save the post pictures
        destination = os.path.join(
            current_app.root_path, 'static/images/post_pictures', new_filename)

        # Resizing the image to a desired size (optional)
        output_size = (1000, 1000)  # Adjust the size as needed
        image = Image.open(file)
        image.thumbnail(output_size)

        # Saving the resized image to the destination folder
        image.save(destination)

        # Returning the filename to store in the database
        return new_filename
    else:
        # It's not a new file upload, returning the existing filename or None
        return file

def save_profile_picture(file):
    if hasattr(file, 'filename') and file.filename != '':
        random_hex = secrets.token_hex(8)
        _, file_extension = os.path.splitext(file.filename)
        new_filename = random_hex + file_extension
        destination = os.path.join(
            current_app.root_path, 'static/images/profile_pictures', new_filename)

        output_size = (600, 600) 
        image = Image.open(file)
        width, height = image.size
        size = min(width, height)
        left = (width - size) / 2
        top = (height - size) / 2
        right = (width + size) / 2
        bottom = (height + size) / 2
        image = image.crop((left, top, right, bottom))
        image.thumbnail(output_size)
        image.save(destination)
        return new_filename
    else:
        return file
    
def save_header_picture(file):
    if hasattr(file, 'filename') and file.filename != '':
        random_hex = secrets.token_hex(8)
        _, file_extension = os.path.splitext(file.filename)
        new_filename = random_hex + file_extension
        destination = os.path.join(
            current_app.root_path, 'static/images/header_pictures', new_filename)

        output_size = (1800, 1800) 
        image = Image.open(file)
        image.thumbnail(output_size)
        image.save(destination)
        return new_filename
    else:
        return file
    

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
    posts = Post.query.order_by(Post.created_at.desc()).all()
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

# Edit_post >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------


@auth_routes.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        print('form is valid')

        post.title=form.title.data
        post.subtitle=form.subtitle.data
        if form.post_pic.data:
            post.post_pic = save_post_picture(form.post_pic.data)
        post.body=form.body.data

        # Update subjects if needed
        if form.subject.data:
            post.subjects.append(form.subject.data)  

        db.session.commit()

        print(f'post updated: {form.title.data}')
        return redirect(url_for('auth.admin_dashboard'))
    return render_template('auth/edit_post.html', current_user=current_user, form=form, post=post)



# SETTING Main Page >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------


@auth_routes.route('/setting')
@login_required
def setting():
    return render_template('auth/setting.html')


# Edit Profile >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@auth_routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    blog = Blog.query.filter_by(id=current_user.id).first()
    form = ProfileForm(obj=blog)
    if form.validate_on_submit():
        print('Profile form is valid')
        blog.blog_title = form.blog_title.data
        blog.blog_subtitle = form.blog_subtitle.data
        blog.blog_about = form.blog_about.data
        blog.author = form.author.data
        db.session.commit()

        return redirect(url_for('auth.admin_dashboard'))
    return render_template('auth/edit_profile.html', current_user=current_user, form=form)

# Edit Profile Picture >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@auth_routes.route('/edit_profile_picture', methods=['GET', 'POST'])
@login_required
def edit_profile_picture():
    blog = Blog.query.filter_by(id=current_user.id).first()
    form = ProfilePicForm(obj=blog)
    if form.validate_on_submit():
        if form.profile_pic.data:
            blog.profile_pic = save_profile_picture(form.profile_pic.data)
        db.session.commit()
        print(f'Header Pic changed/Form was valid; {blog.profile_pic}')
        return redirect(url_for('auth.admin_dashboard'))
    return render_template('auth/edit_profile_picture.html', current_user=current_user, form=form, blog=blog)


# Edit Header Picture >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@auth_routes.route('/edit_header_picture', methods=['GET', 'POST'])
@login_required
def edit_header_picture():
    blog = Blog.query.filter_by(id=current_user.id).first()
    form = HeaderPicForm(obj=blog)
    if form.validate_on_submit():
        if form.header_pic.data:
            blog.header_pic = save_header_picture(form.header_pic.data)
        db.session.commit()
        print(f'Header Pic changed/Form was valid; {form.header_pic.data}')
        return redirect(url_for('auth.admin_dashboard'))
    return render_template('auth/edit_header_picture.html', current_user=current_user, form=form, blog=blog)