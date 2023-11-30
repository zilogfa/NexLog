from flask import render_template, redirect, url_for, request
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_routes
# from app import db
# from app.models import Blog, Post, Comment, Subject

main_routes = Blueprint('main', __name__)

TITLE = "NexLog"

@main_routes.route('/')
def main():
    return render_template('main/main.html', title=TITLE)


@main_routes.route('/about')
def about():
    return render_template('main/about.html', title=TITLE)