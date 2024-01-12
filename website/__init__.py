##Initialisierung der Anwendung und ihre Konfiguration
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialisierung der SQLAlchemy-Datenbank
db = SQLAlchemy()
DB_NAME = "database.db"

# Funktion zur Erstellung der Flask-Anwendung
def create_app():
    app = Flask(__name__) # Erstellen einer Flask-Anwendung
    app.config['SECRET_KEY'] = 'password' # Setzen eines Geheimschlüssels für die Sicherheit
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Konfigurieren der Datenbank-Verbindung
    db.init_app(app) # Initialisieren der Datenbank mit der App
    
    # Importieren der Blueprint-Module für verschiedene Teile der Anwendung
    from .views import views
    from .auth import auth

    # Registrieren der Blueprints mit der Anwendung
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Importieren der Datenbankmodelle
    from .models import User, Event

    # Erstellen der Datenbanktabellen
    with app.app_context():
        db.create_all()
    
    # Initialisieren des Login-Managers
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Festlegen der Standard-Login-Seite
    login_manager.init_app(app)

    # Funktion zum Laden eines Benutzers anhand seiner ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # Holt den Benutzer aus der Datenbank

    return app # Zurückgeben der erstellten Flask-Anwendung

# Funktion zum Erstellen der Datenbank, falls sie noch nicht existiert
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

