# NEXBLOG

## A Content Management System

NexBlog is your favorite place to blog and share comments. Every user gets a unique subdomain (YourName.nexblog.us) secured with SSL HTTPS, powered by Cloudflare and Heroku.

**Published Site:** [nexblog.us](https://nexblog.us)

Our pages are designed to be responsive and user-friendly on both mobile and desktop devices.

### Features

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

### Project Structure

# Please note, for the following section, replace ... with actual paths and filenames

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
└── README.md

```

### Contact the Developer

**Ali Jafarbeglou**

- Website: [www.alijafarbeglou.com](https://www.alijafarbeglou.com)
- Email: zilogfa@live.com
- Phone: 480-669-1000
