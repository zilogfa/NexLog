from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle')
    body = TextAreaField('Body', validators=[DataRequired()])
    post_pic = FileField('Post Picture')
    submit = SubmitField('Post')


class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=60)], render_kw={"placeholder": "Subject Title"})
    description = TextAreaField('Description', validators=[Length(max=100)], render_kw={"placeholder": "About subject.."})
    submit = SubmitField('Submit')    