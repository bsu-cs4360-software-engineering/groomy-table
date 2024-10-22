from flask import Blueprint, render_template, request, redirect, url_for
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from database import db
from models.user import User

new_acc = Blueprint('new_acc', __name__)

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')


@new_acc.route('/create_account', methods = ['GET', 'POST'])
def create_user():
    form = CreateAccountForm()

    if form.validate_on_submit():

        if username_exists(form.username.data) == False and password_match(form.password.data, form.confirm_password.data) == True:

            new_user = User(
                username = form.username.data,
                email    = form.email.data,
                password = generate_password_hash(form.password.data)
            )

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
            
    return render_template('create_account.html', form=form)

def username_exists (input_username : str) -> bool:
    if User.query.filter_by(username = input_username).first():
        return True
    else:
        return False
    
def password_match(password1 : str, password2 : str) -> bool:
    if password1 == password2:
        return True
    else:
        return False