from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for
from flask_login import login_required
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime, timedelta

from database import db
from models.appointment import Appointment
from models.customer import Customer
from models.note import Note
from models.place import Place
from models.note_link import NoteLink
from models.appointment_form import AppointmentForm

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
@login_required
def dashboard():
    now = datetime.now().date()

    appointments = Appointment.query.options(
        joinedload(Appointment.customer) # Load the associated customer
        .joinedload(Customer.places), # Load the Places associated with the Customer
        joinedload(Appointment.note_links) # Load NoteLinks, which access Notes
    ).filter(Appointment.booked == True).order_by(Appointment.date, Appointment.time).all()

    # Soft delete past appointments
    for appointment in appointments:
        if appointment.date < now:
            appointment.booked = False

    db.session.commit()

    valid_appointments = [appt for appt in appointments if appt.date >= now]

    for appointment in valid_appointments:
        appointment.display_time = appointment.time.strftime('%I:%M %p')

    appointments_today = len([appt for appt in valid_appointments if appt.date == now])

    customers = Customer.query.options(
        joinedload(Customer.places)
    ).all()

    return render_template('dash.html',
                            appointments=valid_appointments,
                            appointments_today=appointments_today,
                            customers=customers)

@dash.route('/dashboard/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = Customer.query.options(
        joinedload(Customer.places),
        joinedload(Customer.note_links).joinedload(NoteLink.note)
    ).get(customer_id)

    if not customer:
        return "Customer not found", 404
    
    if request.method == 'POST':
        existing_note_links = {note_link.note.id: note_link for note_link in customer.note_links}
        submitted_notes = request.form.getlist('notes')

        customer.note_links = []

        for note_content in submitted_notes:
            if note_content:
                if existing_note_links:
                    # Get the first note ID to update
                    note_id = list(existing_note_links.keys())[0]
                    note_link = existing_note_links.pop(note_id)
                    note_link.note.content = note_content
                    customer.note_links.append(note_link)
                else: # Create new note
                    new_note = Note(
                        content=note_content,
                        created_by='Admin'
                    )

                    db.session.add(new_note)
                    db.session.commit()

                    new_note_link = NoteLink(
                        note_id=new_note.id,
                        appointment_id=None,
                        customer_id=customer.id
                    )

                    customer.note_links.append(new_note_link)

        db.session.commit()
        return redirect(url_for('dash.dashboard'))
    
    return render_template('edit_customer.html', customer=customer)

@dash.route('/dashboard/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    appointment = Appointment.query.options(
        joinedload(Appointment.customer).joinedload(Customer.places),
        joinedload(Appointment.note_links).joinedload(NoteLink.note)
    ).get(appointment_id)

    if not appointment:
        return "Appointment not found", 404

    if request.method == 'POST':
        appointment_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        appointment_time = datetime.strptime(request.form.get('time'), '%H:%M').time()

        appointment.date = appointment_date
        appointment.time = appointment_time

        # Get existing notes mapped by their IDs
        existing_note_links = {note_link.note.id: note_link for note_link in appointment.note_links}
        submitted_notes = request.form.getlist('notes')

        appointment.note_links = []

        for note_content in submitted_notes:
            if note_content:
                if existing_note_links:
                    # Get the first note ID to update
                    note_id = list(existing_note_links.keys())[0]
                    note_link = existing_note_links.pop(note_id)
                    note_link.note.content = note_content
                    appointment.note_links.append(note_link)
                else: # Create new note
                    new_note = Note(
                        content=note_content,
                        created_by='Admin'
                    )

                    db.session.add(new_note)
                    db.session.commit()

                    new_note_link = NoteLink(
                        note_id=new_note.id,
                        appointment_id=appointment.id,
                        customer_id=None
                    )

                    appointment.note_links.append(new_note_link)

        db.session.commit()
        return redirect(url_for('dash.dashboard'))

    return render_template('edit_appointment.html', appointment=appointment)

@dash.route('/dashboard/delete_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    if request.method == 'POST':
        appointment = Appointment.query.get(appointment_id)

        if appointment:
            appointment.booked = False
            db.session.commit()

            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Appointment not found.'}), 404

@dash.route('/dashboard/search_customer')
@login_required
def search_customer():
    query = request.args.get('query', '').lower()

    if not query:
        return jsonify({'customers': []})
    
    # Find customers whose name contains the query (case-insensitive)
    customers = Customer.query.filter(Customer.name.ilike(f'%{query}%')).all()

    customer_data = []

    for customer in customers:
        customer_data.append({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone_number': customer.phone_number if customer.phone_number else '',
            'street_address': customer.places[0].address if customer.places else '',
            'latitude': customer.places[0].latitude if customer.places else '',
            'longitude': customer.places[0].longitude if customer.places else ''
        })

    return jsonify({'customers': customer_data})

@dash.route('/dashboard/create_appointment', methods=['GET', 'POST'])
@login_required
def create_appointment():
    form = AppointmentForm()

    if form.validate_on_submit():
        if not form.time.data:
            form.name.errors.append('Select a time.')
            return render_template('create_appointment.html', form=form)
        
        if not _is_valid_date(form.date.data):
            form.name.errors.append('Select a date between today and a month from now.')
            return render_template('create_appointment.html', form=form)
        
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

        return redirect(url_for('dash.confirmation'))
    
    return render_template('create_appointment.html', form=form)

@dash.route('/dashboard/confirmation', methods=['GET'])
@login_required
def confirmation():
    appointment_data = session.pop('appointment_data', None)

    if not appointment_data:
        return redirect(url_for('dash.create_appointment'))
    
    appointment_date = datetime.strptime(appointment_data['date'], '%Y-%m-%d').date()
    appointment_time = datetime.strptime(appointment_data['time'], '%I:%M %p').time()

    try:
        # Check if customer already exists (based on email)
        customer = Customer.query.filter_by(email=appointment_data['email']).first()

        if not customer:
            customer = Customer(
                name=appointment_data['name'],
                email=appointment_data['email'],
                phone_number=appointment_data['phone_number']
            )

            db.session.add(customer)
            db.session.commit()

        new_place = Place(
            address=appointment_data['street_address'],
            latitude=appointment_data['latitude'],
            longitude=appointment_data['longitude'],
            customer_id=customer.id # Associate place with existing/new customer
        )

        db.session.add(new_place)

        new_appointment = Appointment(
            customer_id=customer.id,
            date=appointment_date,
            time=appointment_time,
            booked=True
        )

        db.session.add(new_appointment)
        db.session.commit()

        if appointment_data['notes']:
            new_note = Note(
                content=appointment_data['notes'],
                created_by=customer.name
            )

            db.session.add(new_note)
            db.session.commit()

            note_link = NoteLink(
                note_id=new_note.id,
                customer_id=customer.id,
                appointment_id=new_appointment.id
            )

            db.session.add(note_link)

        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()

    return render_template('dash_confirmation.html', appointment=appointment_data)

def _is_valid_date(selected_date):
    today = datetime.today().date()
    min_date = today + timedelta(days=1)
    max_date = today + timedelta(days=30)
    return min_date <= selected_date <= max_date