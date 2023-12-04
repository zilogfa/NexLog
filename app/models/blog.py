from app import db, bcrypt, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



class Blog(db.Model, UserMixin):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    subdomain = db.Column(db.String(100), unique=True, nullable=False)
    blog_title = db.Column(db.String(40), nullable=True)
    blog_subtitle = db.Column(db.String(100), nullable=True)
    blog_about = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(100), nullable=True)
    author_bio = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(20), nullable=True)
    header_pic = db.Column(db.String(20), nullable=True)
    url = db.Column(db.String(60), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    impressions = db.Column(db.Integer, default=0)
    is_block = db.Column(db.Boolean, default=False)

    subjects = relationship('Subject', back_populates='blog')
    posts = relationship('Post', back_populates='blog')
    comments = db.relationship('Comment', back_populates='blog')

    # def set_password(self, password, bcrypt):
    #     self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    











"""
backref -> Only in Parent or Child
back_populate -> both parent and child
"""
