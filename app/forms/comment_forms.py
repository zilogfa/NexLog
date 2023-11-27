from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    body = TextAreaField('Comment', validators=[Length(max=500)], render_kw={"placeholder": "comment"})
    submit = SubmitField('Submit')