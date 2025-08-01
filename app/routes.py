# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from app import db, admin
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

# Blueprint for all routes
bp = Blueprint('routes', __name__)

# -------------------------
# Admin Panel Configuration
# -------------------------

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

# Attach model to admin panel
admin.add_view(UserAdmin(User, db.session))

# -------------------------
# Login Form
# -------------------------

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# -------------------------
# Routes
# -------------------------

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    return redirect(url_for('routes.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

# -------------------------
# Flask-Login Setup
# -------------------------

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'routes.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
