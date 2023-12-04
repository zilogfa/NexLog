from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField #pip install WTForms-SQLAlchemy
from flask_ckeditor import CKEditorField
from app.models import Subject

class PostForm(FlaskForm):
    def __init__(self, blog_id=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if blog_id is not None:
            self.subject.query = Subject.query.filter_by(blog_id=blog_id)
        else:
            self.subject.query = Subject.query
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Title"})
    subtitle = StringField('Subtitle', render_kw={"placeholder": "Subtitle"})
    post_pic = FileField('Post Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'])], render_kw={'class': ''})
    subject = QuerySelectField(
        'Subject',
        query_factory=lambda: Subject.query,
        get_label='name',
        allow_blank=True,
        blank_text='-- no subject --',
        render_kw={"class": "form_query_select"}
    )
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Post')


class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=60)], render_kw={"placeholder": "Subject Title"})
    description = TextAreaField('Description', validators=[Length(max=100)], render_kw={"placeholder": "About subject.."})
    submit = SubmitField('Submit')    