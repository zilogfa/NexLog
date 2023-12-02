class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static'
    SERVER_NAME = 'localhost:8181'
    SESSION_COOKIE_DOMAIN = '.localhost'
    REMEMBER_COOKIE_DOMAIN = '.localhost'
    WTF_CSRF_ENABLED = False
