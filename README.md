# Headless CMS for Personal Blogging

A Flask-based headless Content Management System (CMS) designed for personal blogging, featuring a secure admin panel, a public JSON API, rich text editing, drag-and-drop media uploads, and a custom user dashboard. This project demonstrates full-stack development skills, including backend development with Flask, database management with PostgreSQL, and a modern front-end interface styled with Tailwind CSS. The CMS is deployed on Render with a managed PostgreSQL database.

## Features

- **Admin Panel**: Built with Flask-Admin for managing users, blog posts, pages, and media files with role-based access control (admin vs. regular users).
- **User Dashboard**: A custom `/home` route with a welcome message, statistics (posts, pages, media counts), and quick action widgets.
- **Public JSON API**: RESTful endpoints (`/api/posts`, `/api/pages`) to serve content for front-end integration.
- **Rich Text Editing**: Integrated Quill WYSIWYG editor for creating and editing rich text content.
- **Drag-and-Drop Media Uploads**: Implemented `/uploads` endpoint using Flask-Dropzone for seamless image uploads.
- **User Authentication**: Secure login system with Flask-Login, supporting password hashing and admin-only access.
- **Database Management**: Uses PostgreSQL for both development and production, with Flask-Migrate and a `create_admin.py` script for initialization.
- **Responsive UI**: Styled with Tailwind CSS for a modern, professional look.
- **Deployment**: Hosted on Render with Gunicorn and managed PostgreSQL.

## Tech Stack

- **Backend**: Flask, Flask-Admin, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Flask-WTF, Flask-Dropzone, Flask-JWT-Extended
- **Database**: PostgreSQL (development and production via Render)
- **Frontend**: Tailwind CSS (via CDN), Quill editor, Flask-Dropzone
- **Deployment**: Render, Gunicorn
- **Version Control**: Git, GitHub, Git LFS (for large files)

## Project Structure

```
flask-headless-cms/
├── app/
│   ├── static/
│   │   └── uploads/          # Directory for storing uploaded media files
│   ├── templates/
│   │   ├── admin/
│   │   │   └── model/edit.html  # Custom template for Quill editor
│   │   ├── home.html         # User dashboard template
│   │   ├── login.html        # Login page template
│   │   └── upload.html       # Drag-and-drop upload page
│   ├── __init__.py           # Flask app initialization
│   ├── api.py                # Public JSON API endpoints
│   ├── config.py             # Configuration settings
│   ├── models.py             # Database models (User, Post, Page, Media)
│   └── routes.py             # Admin, upload, and home routes
├── create_admin.py           # Script to initialize database and create admin user
├── .env                      # Environment variables (not tracked)
├── .gitignore                # Git ignore file
├── Procfile                  # Render deployment configuration
├── requirements.txt          # Python dependencies
├── run.py                    # Flask app entry point
└── README.md                 # Project documentation
```

## Setup Instructions (Local Development)

### Prerequisites
- Python 3.10+
- Git
- Git LFS (for large files: https://git-lfs.github.com/)
- A code editor (e.g., VS Code)
- Access to a PostgreSQL database (e.g., Render’s managed PostgreSQL)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/s1ksh110/flask-headless-cms.git
   cd flask-headless-cms
   ```

2. **Install Git LFS**:
   ```bash
   git lfs install
   ```

3. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**:
   Install the required Python packages, including `psycopg2-binary` for PostgreSQL connectivity:
   ```bash
   pip install flask flask-admin flask-sqlalchemy flask-login flask-migrate flask-wtf flask-jwt-extended flask-dropzone python-dotenv psycopg2-binary
   pip freeze > requirements.txt
   ```

5. **Set Up Environment Variables**:
   Create a `.env` file in the project root with your Render PostgreSQL database URL:
   ```plaintext
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://<your-render-postgres-url>
   ```
   Example Render PostgreSQL URL:
   ```plaintext
   postgresql://flaskcms_db_1538_user:QezIg1mXRhbNFrXcYGYPD6VQC84zfdO1@dpg-d26vuu8gjchc73enhtf0-a.oregon-postgres.render.com/flaskcms_db_1538
   ```

6. **Initialize the Database**:
   Run the `create_admin.py` script to drop and recreate tables and create a default admin user:
   ```bash
   python create_admin.py
   ```
   Expected output:
   ```
   ✅ Tables recreated!
   ✅ Admin user created!
   ```

7. **Run Database Migrations**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

8. **Run the Application**:
   ```bash
   python run.py
   ```
   Access the app at `http://localhost:5000`.

9. **Explore Features**:
   - **Login**: Log in at `http://localhost:5000/login` with `admin`/`admin123`.
   - **Dashboard**: View your dashboard at `http://localhost:5000/home`.
   - **API**: Access `http://localhost:5000/api/posts` or `http://localhost:5000/api/pages`.
   - **Media Uploads**: Visit `http://localhost:5000/uploads` for drag-and-drop uploads.

## Deployment (Render)

The project is deployed on Render with a managed PostgreSQL database. Follow these steps:

1. **Push to GitHub**:
   ```bash
   git push origin main
   ```

2. **Create a PostgreSQL Database on Render**:
   - Sign up at [render.com](https://render.com).
   - Create a new PostgreSQL instance and copy the **Internal Database URL**.

3. **Create a Render Web Service**:
   - Create a new Web Service and connect your GitHub repository.
   - Configure:
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn run:app`
   - Add environment variables:
     ```plaintext
     FLASK_ENV=production
     SECRET_KEY=your-secret-key
     DATABASE_URL=<render-postgres-internal-url>
     ```

4. **Initialize the Database**:
   - In the Render shell, run:
     ```bash
     python create_admin.py
     flask db upgrade
     ```

5. **Access the Deployed App**:
   - Available at your Render URL (e.g., `https://your-app.onrender.com`).

## Demo Data

- **Admin User**: Username: `admin`, Password: `admin123` (created via `create_admin.py`).
- **Sample Post**: "My First Blog Post" with content "Welcome to my blog!".
- **Sample Page**: "About Me" with content "Hi, I’m a developer.".
- **Sample Media**: Upload `blog-header.jpg` via `/uploads`.

## API Endpoints

- `GET /api/posts`: Retrieve all posts.
- `GET /api/posts/<id>`: Retrieve a specific post.
- `GET /api/pages`: Retrieve all pages.
- `GET /api/pages/<id>`: Retrieve a specific page.

## Media Uploads

The `/uploads` endpoint uses Flask-Dropzone for drag-and-drop image uploads (PNG, JPG, JPEG, GIF, max 16MB).

## Future Improvements

- Add JWT authentication for API endpoints.
- Implement a front-end (e.g., React) to consume the API.
- Add unit tests for reliability.

## Contributing

Contributions are welcome! Fork the repo, create a feature branch, and submit a pull request.
