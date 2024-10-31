from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required
from sqlalchemy.orm import joinedload

from datetime import datetime

from database import db
from models.appointment import Appointment
from models.note import Note

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
@login_required
def dashboard():
    now = datetime.now().date()

    appointments = Appointment.query.options(
        joinedload(Appointment.places),
        joinedload(Appointment.notes)
    ).filter(Appointment.booked == True).order_by(Appointment.date, Appointment.time).all()

    for appointment in appointments:
        if appointment.date < now:
            appointment.booked = False

    db.session.commit()

    valid_appointments = [appt for appt in appointments if appt.date >= now]

    for appointment in valid_appointments:
        appointment.display_time = appointment.time.strftime('%I:%M %p')

    return render_template('dash.html', appointments=valid_appointments)

@dash.route('/dashboard/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    appointment = Appointment.query.options(
        joinedload(Appointment.places),
        joinedload(Appointment.notes)
    ).get(appointment_id)

    if not appointment:
        return "Appointment not found", 404

    if request.method == 'POST':
        appointment_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        appointment_time = datetime.strptime(request.form.get('time'), '%H:%M').time()

        appointment.date = appointment_date
        appointment.time = appointment_time

        # Get existing notes mapped by their IDs
        existing_notes = {note.id: note for note in appointment.notes}
        submitted_notes = request.form.getlist('notes')

        appointment.notes = []

        for note_content in submitted_notes:
            if note_content:
                if existing_notes:
                    # Get the first note ID to update
                    note_id = list(existing_notes.keys())[0]
                    note = existing_notes[note_id]
                    note.content = note_content
                    appointment.notes.append(note)
                    existing_notes.pop(note_id)
                else: # Create new note
                    new_note = Note(
                        content=note_content,
                        created_by='Admin',
                        appointment_id=appointment.id
                    )

                    appointment.notes.append(new_note)

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