from app import db
from datetime import datetime

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    posts = db.relationship('Post', secondary='post_subject_association', back_populates='subjects')

    post_subject_association = db.Table('post_subject_association',
        db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
        db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
    )