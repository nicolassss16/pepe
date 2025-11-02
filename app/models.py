from . import db
from flask_login import UserMixin

# Relacionamos el user_loader con el modelo User
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    # Relación: Un usuario puede tener muchos tickets
    tickets = db.relationship('Ticket', backref='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    
    # --- ¡COLUMNAS NUEVAS! ---
    # Agregamos las columnas que faltaban
    price = db.Column(db.Float, nullable=False, default=0.0)
    available_tickets = db.Column(db.Integer, nullable=False, default=100)
    # --------------------------

    # Relación: Un evento puede tener muchos tickets
    tickets = db.relationship('Ticket', backref='event', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Nombre del comprador
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Puede ser nulo si compra como invitado
    quantity = db.Column(db.Integer, nullable=False, default=1)
    qr_code = db.Column(db.Text, nullable=False)
    ticket_code = db.Column(db.String(100), unique=True, nullable=False)
    transaction_id = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(50))
    usado = db.Column(db.Boolean, default=False)