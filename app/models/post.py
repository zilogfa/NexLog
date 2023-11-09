from app import db
from app.models.blog import Blog
from sqlalchemy.orm import relationship
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)

    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(150), nullable=True)
    body = db.Column(db.Text, nullable=False)
    post_pic = db.Column(db.String(20), nullable=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    blog = relationship('Blog', back_populates='posts')
    subjects = db.relationship('Subject', secondary='post_subject_association', back_populates='posts')
    comments = db.relationship('Comment', lazy=True)

    # subjects = db.relationship('Subject', backref='posts')