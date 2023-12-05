# NEXBLOG

## A Content Management System

NexBlog is your favorite place to blog and share comments. Every user gets a unique subdomain (YourName.nexblog.us) secured with SSL HTTPS, powered by Cloudflare and Heroku.

**Published Site:** [nexblog.us](https://nexblog.us)

Table of Contents

- [Features](#Features)
- [Languages and Technologies](#Languages)
- [Project Structure](#structure)
- [Contact the Developer](#Contactr)



Our pages are designed to be responsive and user-friendly on both mobile and desktop devices.

## Features

### Home page

- **Landing Page (`main.html`):** Introduction to NexBlog, with visibility to top posts and top blogs from all users.
- **About (`about.html`):** Information about NexBlog.
- **Register (`register.html`):** For creating a new blog.
- **Login (`login.html`):** For user login to their blog.

### Admin Panel

- **Dashboard (`admin_dashboard.html`):** Overview of published posts, blog analytics, engagement stats, and quick access to settings, new post creation, and subject management.
- **Create Subject (`create_subject.html`):** For creating and managing subjects, modifying previous ones, or deleting them.
- **Create Post (`create_post.html`):** For creating new posts with an advanced CKEditor, organizing them by associating them with subjects, and uploading photos for each post.
- **Post Comments (`post_comments.html`):** Where you can view post comments and delete them if needed.
- **Settings:** Access to and modification of profile and blog information such as title, subtitle, bio, author, and customizing the blog by adding or changing the header picture and blog profile/logo image.

### Blog

- **Blog Home (`blog.html`):** Where all published posts are visible, categorized by subjects, and favored by readers.
- **Show Post (`show_post.html`):** Where individual posts can be read, comments viewed, and new comments submitted.


## Languages and Technologies

NexBlog is built using a variety of languages and technologies that ensure a secure, responsive, and user-friendly experience. Here's a breakdown of the core stack:

- **Frontend:**
  - **HTML5:** For structuring content and layout.
  - **CSS3:** For styling and responsive design.
  - **JavaScript:** For dynamic interactions and client-side scripting.

- **Backend:**
  - **Python:** The primary programming language used for server-side logic.
  - **Flask:** A lightweight WSGI web application framework used to serve the backend.
  - **Jinja2:** A template engine for Python, used in conjunction with Flask.

- **Database:**
  - **SQLite:** Used in the development environment for its simplicity and ease of use.
  - **PostgreSQL:** Recommended for production in Heroku for a robust, scalable, and production-ready database solution.

- **Editor and Tools:**
  - **CKEditor:** A powerful WYSIWYG editor integrated for composing blog posts.
  - **Pillow:** A Python Imaging Library that adds image processing capabilities to your Python interpreter.

- **Deployment and Hosting:**
  - **Heroku:** A cloud platform as a service (PaaS) used for deploying and running the application.
  - **Cloudflare:** Provides DNS management, SSL protection, and optimization services.

- **Version Control:**
  - **Git:** For source code management.
  - **GitHub:** A cloud-based hosting service that lets you manage Git repositories.

- **Additional Libraries and Frameworks:**
  - **WTForms:** For form handling and validation.
  - **Flask-WTF:** Integrates Flask with WTForms.
  - **Flask-Login:** For handling user authentication.
  - **Flask-Migrate:** For handling SQLAlchemy database migrations.
  - **Flask-CKEditor:** Flask extension for CKEditor.

These technologies together create a robust platform that balances functionality with developer ergonomics, ensuring that NexBlog is both powerful and maintainable.


## Project Structure


```bash
NEXBLOG
├── app
│   ├── __init__.py
│   ├── forms
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── main_forms.py
│   │   └── comment_forms.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── blog.py
│   │   ├── comment.py
│   │   ├── post.py
│   │   └── subject.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── blog_routes.py
│   │   └── main_routes.py
│   ├── static
│   │   ├── css
│   │   │   └── All style's.css
│   │   ├── images
│   │   │   ├── header_pictures
│   │   │   ├── profile_pictures
│   │   │   ├── post_pictures
│   │   │   └── main
│   │   └── js
│   │       ├── delete_post.js
│   │       ├── delete_subject.js
│   │       └── index.js
│   └── templates
│       └── All HTML's templates
├── config.py
├── run.py
├── .gitignore
├── Procfile
├── requirments.txt
└── README.md

```

## Contact the Developer

**Ali Jafarbeglou**

- Website: [www.alijafarbeglou.com](https://www.alijafarbeglou.com)
- Email: zilogfa@live.com
- Phone: 480-669-1000
