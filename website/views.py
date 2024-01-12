from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask import current_app
from .models import Event, Zusage
from . import db
import json
from datetime import datetime

# Erstellen eines Blueprint, einer Art Unteranwendung für Flask
views = Blueprint('views', __name__)

# Route für die Startseite, reagiert auf GET- und POST-Anfragen
@views.route('/', methods=['GET', 'POST'])
@login_required #home nur aufrufbar wenn eingeloggt
def home():
    # Überprüfen, ob die Anfrage vom Typ POST ist (Formulardaten gesendet)
    if request.method == 'POST':
        # Daten aus dem Formular extrahieren
        event_type = request.form.get('event_type')
        event_time = request.form.get('event_time')
        location = request.form.get('location')
        description = request.form.get('description')

        # Überprüfen, ob alle Formularfelder ausgefüllt sind
        if not event_type or not event_time or not location or not description:
            flash('Bitte füllen Sie alle Felder aus!', category='error')
        else:
            try:
                # Erstellen eines neuen Event-Objekts und Speichern in der Datenbank
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

    # Render des Home-Templates (HTML-Seite)
    return render_template("home.html", current_user=current_user)

# Route für die Übersichtsseite
@views.route('/uebersicht')
@login_required
def uebersicht():
    # Hier nehmen wir an, dass `current_user.events` die Events enthält, die dem Spieler angezeigt werden sollen
    events = current_user.events
    # Render des Übersichts-Templates (HTML-Seite)
    return render_template("events.html", events=events)

# Route für die Verarbeitung von Zusagen und Absagen
@views.route('/event-response', methods=['POST'])
@login_required
def event_response():
    # Daten aus der AJAX-Anfrage extrahieren
    data = request.get_json()
    event_id = data['event_id']
    status = data['response']  # 'zusage' oder 'absage'

    # Suchen Sie nach einer vorhandenen Zusage/Absage für dieses Event vom aktuellen Benutzer
    existing_response = Zusage.query.filter_by(user_id=current_user.id, event_id=event_id).first()

    # Wenn keine Antwort existiert, erstelle eine neue; andernfalls aktualisiere die existierende
    if not existing_response:
        new_response = Zusage(user_id=current_user.id, event_id=event_id, status=status)
        db.session.add(new_response)
    else:
        existing_response.status = status

    # Änderungen in der Datenbank speichern
    db.session.commit()

    flash(f"Du hast {'zugesagt' if status == 'zusage' else 'abgesagt'}!", category='success')
    return "ok"

# Route zum Löschen von Events
@views.route('/delete-event', methods=['POST'])
def delete_event():
    # Daten aus der AJAX-Anfrage extrahieren
    event = json.loads(request.data)
    eventId = event['eventId']

    # Event suchen und löschen, falls es dem aktuellen Benutzer gehört
    event = Event.query.get(eventId)
    if event:
        if event.user_id == current_user.id:
            db.session.delete(event)
            db.session.commit()

    # Leere JSON-Antwort senden
    return jsonify({}) ##empty response
    

