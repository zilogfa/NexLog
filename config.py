class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER = 'static'
    SERVER_NAME = 'localhost:5000'
    SESSION_COOKIE_DOMAIN = '.localhost'
    REMEMBER_COOKIE_DOMAIN = '.localhost'
    