import os

class Config:
    SERVER_NAME = 'nexlog.us'
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static'
    WTF_CSRF_ENABLED = False
    # if os.environ.get('FLASK_ENV') == 'production':
    #     SERVER_NAME = 'nexlog.us'
    # else:
    #     SERVER_NAME = 'nexlog-c4d6a2de71db.herokuapp.com'
    SESSION_COOKIE_DOMAIN = '.nexlog.us'
    REMEMBER_COOKIE_DOMAIN = '.nexlog.us'
    
