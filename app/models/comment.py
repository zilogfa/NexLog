from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    name = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    post = db.relationship('Post', back_populates='comments')
    blog = db.relationship('Blog', back_populates='comments')
    
    # blog = relationship('Blog', back_populates='comments')


 