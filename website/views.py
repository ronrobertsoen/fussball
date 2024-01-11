from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask import current_app
from .models import Event, Zusage
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required #home nur aufrufbar wenn eingeloggt
def home():
    if request.method == 'POST':
        event_type = request.form.get('event_type')
        event_time = request.form.get('event_time')
        location = request.form.get('location')
        description = request.form.get('description')

        if not event_type or not event_time or not location or not description:
            flash('Bitte füllen Sie alle Felder aus!', category='error')
        else:
            try:
                new_event = Event(
                    event_type=event_type,
                    description=description,
                    event_time=datetime.strptime(event_time, '%Y-%m-%dT%H:%M'),
                    location=location,
                    user_id=current_user.id
                )
                db.session.add(new_event)
                db.session.commit()
                flash('Event hinzugefügt!', category='success')
            except ValueError:
                flash('Falsches Datumsformat!', category='error')

    return render_template("home.html", current_user=current_user)

@views.route('/uebersicht')
@login_required
def uebersicht():
    # Hier nehmen wir an, dass `current_user.events` die Events enthält, die dem Spieler angezeigt werden sollen
    events = current_user.events
    return render_template("events.html", events=events)

@views.route('/event-response', methods=['POST'])
@login_required
def event_response():
    data = request.get_json()
    event_id = data['event_id']
    status = data['response']  # 'zusage' oder 'absage'

    # Suchen Sie nach einer vorhandenen Zusage/Absage für dieses Event vom aktuellen Benutzer
    existing_response = Zusage.query.filter_by(user_id=current_user.id, event_id=event_id).first()

    if not existing_response:
        new_response = Zusage(user_id=current_user.id, event_id=event_id, status=status)
        db.session.add(new_response)
    else:
        existing_response.status = status

    db.session.commit()

    flash(f"Du hast {'zugesagt' if status == 'zusage' else 'abgesagt'}!", category='success')
    return "ok"

@views.route('/delete-event', methods=['POST'])
def delete_event():
    event = json.loads(request.data)
    eventId = event['eventId']
    event = Event.query.get(eventId)
    if event:
        if event.user_id == current_user.id:
            db.session.delete(event)
            db.session.commit()
            
    return jsonify({}) ##empty response
    

