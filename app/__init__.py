from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_bcrypt import Bcrypt








app = Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


from app.models import Blog
@login_manager.user_loader
def load_user(blog_id):
    return Blog.query.get(int(blog_id))

# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     return redirect(url_for('auth.login', _external=True, _scheme='http'))

# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     # Redirect unauthorized users to the login page, preserving subdomain
#     if 'localhost' in request.host or '127.0.0.1' in request.host:
#         # Special handling for localhost
#         if 'localhost' in request.host:
#             parts = request.host.split('.')
#             if len(parts) > 1:
#                 subdomain = parts[0]
#     else:
#         subdomain = request.host.split('.')[0]
#     if subdomain:
#         login_manager.login_view = f'{subdomain}.auth.login'
#         # return redirect(url_for(f'{subdomain}.auth.login', _external=True, _scheme='http')) 
#     print("\n\nFull URL:", request.url)   
#     return redirect(url_for('auth.login', _external=True, _scheme='http', subdomain=subdomain))


# app.config['SERVER_NAME'] = 'localhost:5000'


# @app.before_request
# def before_request():
#     print(request)
#     print("Full URL:", request.url)
#     print("Host:", request.host)
#     subdomain = None
#     if 'localhost' in request.host or '127.0.0.1' in request.host:
#         # Special handling for localhost
#         if 'localhost' in request.host:
#             parts = request.host.split('.')
#             if len(parts) > 1:
#                 subdomain = parts[0]
#     else:
#         subdomain = request.host.split('.')[0]
        
#     if subdomain:
#         print("Subdomain:", subdomain)
#         login_manager.login_view = f'{subdomain}.auth.login'
#     else:
#         print("No subdomain in request")
#         login_manager.login_view = 'auth.login'

      

        



from app.models import Blog # Importing to avoid circular import
from app.routes import main_routes, auth_routes, blog_routes
app.register_blueprint(main_routes)
app.register_blueprint(auth_routes,url_prefix='/auth')
app.register_blueprint(blog_routes,url_prefix='/blog')









'''
url_prefix='/auth'
'''