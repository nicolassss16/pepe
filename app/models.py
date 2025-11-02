from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    # --- LÍNEA NUEVA ---
    # Agrega esta columna para el rol de administrador
    is_admin = db.Column(db.Boolean, default=False)
    # ------------------
    
    # Relación (inversa) con Ticket
    tickets = db.relationship('Ticket', back_pop='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    # --- LÍNEAS NUEVAS ---
    # Agrega estas columnas que faltaban
    price = db.Column(db.Float, nullable=False, default=0.0)
    available_tickets = db.Column(db.Integer, nullable=False, default=100)
    # ---------------------

    # Relación (inversa) con Ticket
    tickets = db.relationship('Ticket', back_pop='event', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    qr_code = db.Column(db.Text, nullable=False) # Base64 del QR
    ticket_code = db.Column(db.String(100), unique=True, nullable=False) # UUID
    transaction_id = db.Column(db.String(100), nullable=False) # Para agrupar compras
    payment_method = db.Column(db.String(50))
    usado = db.Column(db.Boolean, default=False)
    
    # --- Claves Foráneas ---
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Puede ser null si compra sin loguearse
    
    # --- Relaciones ---
    event = db.relationship('Event', back_pop='tickets')
    user = db.relationship('User', back_pop='tickets')
