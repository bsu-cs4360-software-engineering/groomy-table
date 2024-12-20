import stripe
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy.orm import joinedload

from datetime import datetime, time, timedelta

from database import db
from models.appointment import Appointment, AppointmentStatus
from models.customer import Customer
from models.place import Place
from models.note import Note
from models.note_link import NoteLink
from models.appointment_form import AppointmentForm
from models.invoice import Invoice
from models.service import Service

appts = Blueprint('appts', __name__)

@appts.route('/appointments', methods=['GET', 'POST'])
def appointments():
    form = AppointmentForm()

    if form.validate_on_submit():
        if not form.time.data:
            return render_template('appointments.html', form=form)
        
        date = datetime.strptime(form.date.data, '%Y-%m-%d').date()

        # Validate the selected date
        if not _is_valid_date(date):
            form.name.errors.append('Select a date between today and a month from now.')
            return render_template('appointments.html', form=form)
        
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        session['appointment_data'] = {
            'name': form.name.data,
            'email': form.email.data,
            'phone_number': form.phone_number.data,
            'street_address': form.street_address.data,
            'date': date.isoformat(),
            'time': form.time.data,
            'notes': form.notes.data,
            'latitude': latitude,
            'longitude': longitude
        }

        return redirect(url_for('appts.invoice'))
    
    return render_template('appointments.html', form=form)

@appts.route('/available_slots', methods=['GET'])
def available_slots():
    date_str = request.args.get('date')
    
    # Parse the date string into a date object
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Fetch appointments for the selected date
    appointments = db.query(Appointment).filter_by(date=date).all()

    # Create a list of all possible time slots (9 AM to 5 PM)
    time_slots = [time(hour=hour) for hour in range(9, 18, 2)]
    available_slots = []

    for slot in time_slots:
        booked = any(app.time == slot for app in appointments)
        available_slots.append({
            'time': slot.strftime('%I:%M %p'),
            'booked': booked
        })

    return jsonify(available_slots)

@appts.route('/invoice', methods=['GET', 'POST'])
def invoice():
    appointment_data = session.get('appointment_data')

    if not appointment_data:
        return redirect(url_for('appts.appointments'))

    invoice_id = session.get('invoice_id')
    services = db.query(Service).options(
        joinedload(Service.note_links)
    ).all()
    

    if invoice_id:
        invoice_to_display = db.query(Invoice).get_or_404(invoice_id)
        invoice_to_display.customer_name = appointment_data['name']
        invoice_to_display.customer_address = appointment_data['street_address']
        db.commit()
    else:
        new_invoice = Invoice(
            customer_name=appointment_data['name'],
            customer_address=appointment_data['street_address'],
        )
        db.add(new_invoice)
        db.commit()
        session['invoice_id'] = new_invoice.id
        invoice_to_display = new_invoice

    return render_template('invoice.html', appointment_data=appointment_data, invoice_info=invoice_to_display, services=services)

@appts.route('/payment', methods=['GET', 'POST'])
def payment():
    appointment_data = session.get('appointment_data')

    if not appointment_data:
        return redirect(url_for('appts.appointments'))
    
    if request.method == 'POST':
        try:
            amount = 1000
            description = f"Appointment Booking Charge for {appointment_data['name']}"

            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                description=description,
                payment_method=request.json['payment_method_id'],
                confirm=True,
                capture_method="manual",
                return_url=url_for('appts.confirmation', _external=True)
            )

            appointment_data['payment_intent_id'] = payment_intent['id']
            session['appointment_data'] = appointment_data

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

    try:
        # Check if customer already exists (based on email)
        customer = db.query(Customer).filter_by(email=appointment_data['email']).first()

        if not customer:
            customer = Customer(
                name=appointment_data['name'],
                email=appointment_data['email'],
                phone_number=appointment_data['phone_number']
            )

            db.add(customer)
            db.commit()

        new_place = Place(
            address=appointment_data['street_address'],
            latitude=appointment_data['latitude'],
            longitude=appointment_data['longitude'],
            customer_id=customer.id # Associate place with existing/new customer
        )

        db.add(new_place)

        new_appointment = Appointment(
            customer_id=customer.id,
            date=appointment_date,
            time=appointment_time,
            payed=False,
            status=AppointmentStatus.OPEN,
            payment_intent_id=appointment_data['payment_intent_id']
        )

        db.add(new_appointment)
        db.commit()

        if appointment_data['notes']:
            new_note = Note(
                content=appointment_data['notes'],
                created_by=customer.name
            )

            db.add(new_note)
            db.commit()

            note_link = NoteLink(
                note_id=new_note.id,
                customer_id=None,
                appointment_id=new_appointment.id
            )

            db.add(note_link)

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()

    return render_template('confirmation.html', appointment=appointment_data)

def _is_valid_date(selected_date):
    today = datetime.today().date()
    min_date = today + timedelta(days=1)
    max_date = today + timedelta(days=30)
    return min_date <= selected_date <= max_date