class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static'
    SERVER_NAME = 'nexlog.us'
    SERVER_NAME = 'nexlog-c4d6a2de71db.herokuapp.com'
    # SESSION_COOKIE_DOMAIN = '.nexlog.us'
    # REMEMBER_COOKIE_DOMAIN = '.nexlog.us'
    WTF_CSRF_ENABLED = False
