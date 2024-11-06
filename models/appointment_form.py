from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, HiddenField, TextAreaField, TelField
from wtforms.validators import DataRequired, Optional, Email

class AppointmentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone_number = TelField('Phone Number', validators=[Optional()])
    street_address = StringField('Street Address', validators=[DataRequired()])
    date = DateField('Select Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = HiddenField('Appointment Time', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])