from flask import Blueprint, render_template, redirect, url_for
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash

from database import db
from models.user import User
from models.password import UserPass

new_acc = Blueprint('new_acc', __name__)

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

@new_acc.route('/create_account', methods = ['GET', 'POST'])
def create_user():
    form = CreateAccountForm()

    if form.validate_on_submit():

        if _username_exists(form.username.data) == True:
            form.username.errors.append("Username taken.")
        elif _email_exists(form.email.data) == True:
            form.username.errors.append("Email already in use.")
        elif _passwords_match(form.password.data, form.confirm_password.data) == False:
            form.username.errors.append("Passwords do not match.")
        else:
            new_pass = UserPass(password_hash=generate_password_hash(form.password.data))
            db.session.add(new_pass)
            db.session.flush()

            new_user = User(
                username    = form.username.data,
                email       = form.email.data,
                password_id = new_pass.id
            )

            db.session.add(new_user)
            db.session.add(new_pass)
            db.session.commit()
            return redirect(url_for('auth.login'))
            
    return render_template('create_account.html', form=form)

def _username_exists(input_username : str) -> bool:
    if User.query.filter_by(username = input_username).first():
        return True
    else:
        return False
    
def _email_exists(input_email : str) -> bool:
    if User.query.filter_by(email = input_email).first():
        return True
    else:
        return False
    
def _passwords_match(password1 : str, password2 : str) -> bool:
    if password1 == password2:
        return True
    else:
        return False