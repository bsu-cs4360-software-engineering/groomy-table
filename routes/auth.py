from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from models.user import User

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data
        user_username = User.query.filter_by(username=username_or_email).first()
        user_email = User.query.filter_by(email=username_or_email).first()

        if user_username and check_password_hash(user_username.password, password):
            login_user(user_username)
            return redirect(url_for('dash.dashboard'))
        elif user_email and check_password_hash(user_email.password, password):
            login_user(user_email)
            return redirect(url_for('dash.dashboard'))
        else:
            form.username_or_email.errors.append("Invalid username or password.")
        
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))