import stripe
from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime, timedelta

from database import db
from models.appointment import Appointment, AppointmentStatus
from models.customer import Customer
from models.note import Note
from models.place import Place
from models.note_link import NoteLink
from models.appointment_form import AppointmentForm
from models.service import Service

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('dash.appointments'))

@dash.route('/dashboard/appointments')
@login_required
def appointments():
    now = datetime.now().date()

    appointments = db.query(Appointment).options(
        db.joinedload((Appointment.customer, Customer.places)), # Load the Places associated with the Customer
        db.joinedload(Appointment.note_links) # Load NoteLinks, which access Notes
    ).order_by(Appointment.date, Appointment.time).all()

    # Soft delete past appointments
    for appointment in appointments:
        if appointment.date < now:
            appointment.status = AppointmentStatus.COMPLETE

    db.commit()

    valid_appointments = [appt for appt in appointments if appt.date >= now]

    for appointment in valid_appointments:
        name_parts = appointment.customer.name.split(' ', 1)
        appointment.fname = name_parts[0]
        appointment.lname = name_parts[1] if len(name_parts) > 1 else ""
        appointment.display_date = appointment.date.strftime('%d-%b-%Y')
        appointment.display_time = appointment.time.strftime('%I:%M %p')

    appointments_today = len([appt for appt in valid_appointments if appt.date == now])

    customers = db.query(Customer).options(
        db.joinedload(Customer.places)
    ).all()

    return render_template('manage_appointments.html',
                            appointments=valid_appointments,
                            appointments_today=appointments_today,
                            customers=customers,
                            user=current_user)

@dash.route('/dashboard/services')
@login_required
def services():
    services = db.query(Service).options(
        db.joinedload(Service.note_links)
    ).all()

    valid_services = [service for service in services if service.deleted != True]

    return render_template('manage_services.html',
                            services=valid_services,
                            user=current_user)

@dash.route('/dashboard/add_service', methods=['GET', 'POST'])
@login_required
def new_service():
    if request.method == 'POST':

        service = Service(
            name=request.form['name'],
            description=request.form['description'],
            price='is_addon' in request.form,
            is_package='is_package' in request.form
        )

        db.add(service)
        db.commit()

        return redirect(url_for('dash.services'))
    
    return render_template('new_service.html',
                            user=current_user)

@dash.route('/dashboard/edit_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = db.query(Service).options(
        db.joinedload(Service.note_links).joinedload(NoteLink.note)
    ).get(service_id)

    if not service:
        return "Service not found", 404
    
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        service.price = request.form['price']
        service.is_addon = 'is_addon' in request.form
        service.is_package = 'is_package' in request.form

        existing_note_links = {note_link.note.id: note_link for note_link in service.note_links}
        submitted_notes = request.form.getlist('notes')

        service.note_links = []

        for note_content in submitted_notes:
            if note_content:
                if existing_note_links:
                    # Get the first note ID to update
                    note_id = list(existing_note_links.keys())[0]
                    note_link = existing_note_links.pop(note_id)
                    note_link.note.content = note_content
                    service.note_links.append(note_link)
                else: # Create new note
                    new_note = Note(
                        content=note_content,
                        created_by=current_user.username
                    )

                    db.add(new_note)
                    db.commit()

                    new_note_link = NoteLink(
                        note_id=new_note.id,
                        appointment_id=None,
                        customer_id=None,
                        service_id=service.id
                    )

                    service.note_links.append(new_note_link)

        db.commit()
        return redirect(url_for('dash.services'))
    
    return render_template('edit_service.html', 
                            service=service,
                            user=current_user)

@dash.route('/dashboard/delete_service/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    if request.method == 'POST':
        service = db.query(Service).get(service_id)

        if service:
            service.deleted = True
            db.commit()

            return redirect(url_for('dash.services'))
        else:
            return jsonify({'error': 'Service not found.'}), 404

@dash.route('/dashboard/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = db.query(Customer).options(
        db.joinedload(Customer.places),
        db.joinedload(Customer.note_links).joinedload(NoteLink.note)
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

                    db.add(new_note)
                    db.commit()

                    new_note_link = NoteLink(
                        note_id=new_note.id,
                        appointment_id=None,
                        customer_id=customer.id
                    )

                    customer.note_links.append(new_note_link)

        db.commit()
        return redirect(url_for('dash.dashboard'))
    
    return render_template('edit_customer.html', customer=customer)

@dash.route('/dashboard/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    appointment = db.query(Appointment).options(
        db.joinedload(Appointment.customer).joinedload(Customer.places),
        db.joinedload(Appointment.note_links).joinedload(NoteLink.note)
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

                    db.add(new_note)
                    db.commit()

                    new_note_link = NoteLink(
                        note_id=new_note.id,
                        appointment_id=appointment.id,
                        customer_id=None
                    )

                    appointment.note_links.append(new_note_link)

        db.commit()
        return redirect(url_for('dash.dashboard'))

    return render_template('edit_appointment.html', appointment=appointment)

@dash.route('/dashboard/delete_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    if request.method == 'POST':
        appointment = db.query(Appointment).get(appointment_id)

        if appointment:
            appointment.status = AppointmentStatus.DELETED
            db.commit()

            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Appointment not found.'}), 404

@dash.route('/dashboard/book_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def book_appointment(appointment_id):
    appointment = db.query(Appointment).get(appointment_id)

    if appointment.status != AppointmentStatus.OPEN:
        return jsonify({'error': 'Appointment not in an open state.'})
    
    # Mark appointment as accepted
    appointment.status = AppointmentStatus.BOOKED
    db.commit()

@dash.route('/dashboard/search_customer')
@login_required
def search_customer():
    query = request.args.get('query', '').lower()

    if not query:
        return jsonify({'customers': []})
    
    # Find customers whose name contains the query (case-insensitive)
    customers = db.query(Customer).filter(Customer.name.ilike(f'%{query}%')).all()

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
            status=AppointmentStatus.BOOKED
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
                customer_id=customer.id,
                appointment_id=new_appointment.id
            )

            db.add(note_link)

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()

    return render_template('dash_confirmation.html', appointment=appointment_data)

def _is_valid_date(selected_date):
    today = datetime.today().date()
    min_date = today + timedelta(days=1)
    max_date = today + timedelta(days=30)
    return min_date <= selected_date <= max_date