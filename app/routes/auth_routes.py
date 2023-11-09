from flask import render_template, redirect, url_for, request, flash, jsonify
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_manager

from app import db, bcrypt
from app.models import Blog, Subject, Post, Comment
from app.forms.auth_forms import LoginForm, RegistrationForm
from app.forms.post_forms import PostForm, SubjectForm
from app.routes.blog_routes import blog_routes
from . import auth_routes

auth_routes = Blueprint('auth', __name__)



### Login >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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


### Register >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("\n**Registeration for is Validate\n")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        blog = Blog(
            email=(form.email.data).lower(), 
            password = hashed_password,
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

### LogOut >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------
@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.main'))



### Admin Dashboard >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------
@auth_routes.route('/admin_dashboard')
@login_required
def admin_dashboard():
    # if current_user.subdomain != user_subdomain:
    #     return redirect(url_for('main.index'))
    return render_template('auth/admin_dashboard.html', current_user=current_user)


### Create_subject >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -----------------------------------------------------------------
@auth_routes.route('/create_subject', methods=['GET', 'POST'])
@login_required
def create_subject():
    form = SubjectForm()
    subjects = Subject.query.all()
    if form.validate_on_submit():
        print('form is valid')
        new_subject = Subject(
            name = form.name.data,
            description = form.description.data
        )
        db.session.add(new_subject)
        db.session.commit()
        print(f'New subject added: {form.name.data}')
        return redirect(url_for('auth.create_subject'))
    return render_template('auth/create_subject.html', current_user=current_user, form=form, subjects=subjects)

### Edit_subject >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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

### DELETE_subject >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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
