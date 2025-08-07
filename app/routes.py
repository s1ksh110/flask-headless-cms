# routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from app import db, admin, login_manager
from app.models import User, Post, Page, Media
import os

bp = Blueprint('routes', __name__)

# ---- Admin Views ----

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('routes.login'))

class UserAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('routes.login'))

class PostAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('routes.login'))

    form_overrides = {'content': TextAreaField}
    form_args = {'content': {'render_kw': {'class': 'quill-editor'}}}

    def on_model_change(self, form, model, is_created):
        if is_created and not model.user_id:
            model.user_id = current_user.id

class PageAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('routes.login'))

    form_overrides = {'content': TextAreaField}
    form_args = {'content': {'render_kw': {'class': 'quill-editor'}}}

    def on_model_change(self, form, model, is_created):
        if is_created and not model.user_id:
            model.user_id = current_user.id

class MediaAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('routes.login'))

# Register views to admin panel
admin.add_view(UserAdmin(User, db.session))
admin.add_view(PostAdmin(Post, db.session))
admin.add_view(PageAdmin(Page, db.session))
admin.add_view(MediaAdmin(Media, db.session))

# ---- Auth & Forms ----

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---- Routes ----

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    return redirect(url_for('routes.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('routes.home'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

@bp.route('/home')
@login_required
def home():
    # Fetch counts for statistics
    post_count = Post.query.count()
    page_count = Page.query.count()
    media_count = Media.query.count()

    return render_template('home.html', 
                          username=current_user.username,
                          post_count=post_count,
                          page_count=page_count,
                          media_count=media_count)

# ---- File Upload ----

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)

            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            # Save media info in DB
            media = Media(filename=filename, filepath=filepath, user_id=current_user.id)
            db.session.add(media)
            db.session.commit()

            return jsonify({'message': 'File uploaded successfully'}), 200

        return jsonify({'error': 'Invalid file type'}), 400

    return render_template('upload.html')