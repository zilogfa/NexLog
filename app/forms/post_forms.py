from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Title"})
    subtitle = StringField('Subtitle', render_kw={"placeholder": "Subtitle"})
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Post')


class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=60)], render_kw={"placeholder": "Subject Title"})
    description = TextAreaField('Description', validators=[Length(max=100)], render_kw={"placeholder": "About subject.."})
    submit = SubmitField('Submit')    