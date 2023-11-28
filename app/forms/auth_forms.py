from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    subdomain = StringField('Blog Subdomain', validators=[DataRequired()])
    blog_title = StringField('Blog title', validators=[DataRequired(), Length(max=40)])
    blog_subtitle = StringField('Blog title', validators=[Length(max=100)])
    author = StringField('Author Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, message='Select a stronger password.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ProfileForm(FlaskForm):
    blog_title = StringField('Blog title', validators=[DataRequired(), Length(max=40)])
    blog_subtitle = StringField('Blog title', validators=[Length(max=100)])
    blog_about = TextAreaField('Comment', validators=[Length(max=500)], render_kw={"placeholder": "About Blog"})
    author = StringField('Author Name', validators=[DataRequired()])
    submit = SubmitField('Submit')    