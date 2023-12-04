class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static'
    SERVER_NAME = 'nexlog.us'
    # SESSION_COOKIE_DOMAIN = '.nexlog.us'
    # REMEMBER_COOKIE_DOMAIN = '.nexlog.us'
    WTF_CSRF_ENABLED = False
