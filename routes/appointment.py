import stripe
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Optional, Email

from datetime import datetime, time, timedelta

from database import db
from models.appointment import Appointment
from models.place import Place
from models.note import Note

appts = Blueprint('appts', __name__)

class AppointmentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[Optional()])
    street_address = StringField('Street Address', validators=[DataRequired()])
    date = DateField('Select Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = HiddenField('Appointment Time')
    notes = TextAreaField('Notes', validators=[Optional()])

@appts.route('/appointments', methods=['GET', 'POST'])
def appointments():
    form = AppointmentForm()

    if form.validate_on_submit():
        # Validate the selected date
        if not is_valid_date(form.date.data):
            form.date.errors.append('Select a date between today and a month from now.')
            return render_template('appointments.html', form=form)
        
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        session['appointment_data'] = {
            'name': form.name.data,
            'email': form.email.data,
            'phone_number': form.phone_number.data,
            'street_address': form.street_address.data,
            'date': form.date.data.isoformat(),
            'time': form.time.data,
            'notes': form.notes.data,
            'latitude': latitude,
            'longitude': longitude
        }

        return redirect(url_for('appts.payment'))
    
    return render_template('appointments.html', form=form)

@appts.route('/available_slots', methods=['GET'])
def available_slots():
    date_str = request.args.get('date')
    
    # Parse the date string into a date object
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Fetch appointments for the selected date
    appointments = Appointment.query.filter_by(date=date).all()

    # Create a list of all possible time slots (9 AM to 5 PM)
    time_slots = [time(hour=hour) for hour in range(9, 18)]
    available_slots = []

    for slot in time_slots:
        booked = any(app.time == slot for app in appointments)
        available_slots.append({
            'time': slot.strftime('%I:%M %p'),
            'booked': booked
        })

    return jsonify(available_slots)

@appts.route('/payment', methods=['GET', 'POST'])
def payment():
    appointment_data = session.get('appointment_data')

    if not appointment_data:
        return redirect(url_for('appts.appointments'))
    
    if request.method == 'POST':
        try:
            amount = 1000
            token = request.json.get('token')
            description = f"Appointment Booking Charge for {appointment_data['name']}"

            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description=description
            )

            return jsonify({'redirect_url': url_for('appts.confirmation')})
    
        except stripe.error.StripeError as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    return render_template('payment.html', appointment_data=appointment_data)

@appts.route('/confirmation', methods=['GET'])
def confirmation():
    appointment_data = session.pop('appointment_data', None)

    if not appointment_data:
        return redirect(url_for('appts.appointments'))
    
    appointment_date = datetime.strptime(appointment_data['date'], '%Y-%m-%d').date()
    appointment_time = datetime.strptime(appointment_data['time'], '%I:%M %p').time()

    new_place = Place(
        address=appointment_data['street_address'],
        latitude=appointment_data['latitude'],
        longitude=appointment_data['longitude']
    )

    new_appointment = Appointment(
        client=appointment_data['name'],
        email=appointment_data['email'],
        phone_number=appointment_data['phone_number'],
        date=appointment_date,
        time=appointment_time,
        booked=True,
        places=[new_place]
    )

    if appointment_data['notes']:
        new_note = Note(
            content=appointment_data['notes'],
            created_by=new_appointment.client
        )

        new_appointment.notes.append(new_note)

    db.session.add(new_appointment)
    db.session.commit()

    return render_template('confirmation.html', appointment=appointment_data)

def is_valid_date(selected_date):
    today = datetime.today().date()
    max_date = today + timedelta(days=30)
    return today <= selected_date <= max_date