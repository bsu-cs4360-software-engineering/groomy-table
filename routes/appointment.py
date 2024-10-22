from flask import Blueprint, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Optional

from datetime import datetime, time as dt_time

from database import db
from models.appointment import Appointment
from models.place import Place
from models.note import Note

appts = Blueprint('appts', __name__)

class AppointmentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[Optional()])
    street_address = StringField('Street Address', validators=[DataRequired()])
    date = DateField('Select Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = HiddenField('Time')
    notes = TextAreaField('Notes', validators=[Optional()])

@appts.route('/appointments', methods=['GET', 'POST'])
def appointments():
    form = AppointmentForm()

    if form.validate_on_submit():
        appointment_date = form.date.data
        appointment_time = datetime.strptime(form.time.data, '%I:%M %p').time()

        new_place = Place(
            address=form.street_address.data,
            latitude=request.form.get('latitude'),
            longitude=request.form.get('longitude')
        )

        new_appointment = Appointment(
            client=form.name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            date=appointment_date,
            time=appointment_time,
            booked=True,
            places=[new_place]
        )

        if form.notes.data:
            new_note = Note(
                content=form.notes.data,
                created_by=new_appointment.client
            )

            new_appointment.notes.append(new_note)

        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify({'message': 'Appointment booked successfully!'})
    
    return render_template('appointments.html', form=form)

@appts.route('/available_slots', methods=['GET'])
def available_slots():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date parameter is required'}), 400
    
    # Parse the date string into a date object
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Fetch appointments for the selected date
    appointments = Appointment.query.filter_by(date=date).all()

    # Create a list of all possible time slots (9 AM to 5 PM)
    time_slots = [dt_time(hour=hour) for hour in range(9, 18)]
    available_slots = []

    for slot in time_slots:
        booked = any(app.time == slot for app in appointments)
        available_slots.append({
            'time': slot.strftime('%I:%M %p'),
            'booked': booked
        })

    return jsonify(available_slots)