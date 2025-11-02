from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Importamos el login_manager desde la app principal ( __init__.py )
from . import login_manager 

db = SQLAlchemy()

# --- Conectamos el login_manager con el modelo User ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# -----------------------------------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relación (inversa) con Ticket
    # CORREGIDO: back_pop -> back_populates
    tickets = db.relationship('Ticket', back_populates='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    available_tickets = db.Column(db.Integer, nullable=False, default=100)

    # Relación (inversa) con Ticket
    # CORREGIDO: back_pop -> back_populates
    tickets = db.relationship('Ticket', back_populates='event', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False) # Nombre del comprador
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
    # CORREGIDO: back_pop -> back_populates
    event = db.relationship('Event', back_populates='tickets')
    user = db.relationship('User', back_populates='tickets')
```eof

Por favor, reemplaza el contenido de tu `app/models.py` con este.

**Recordatorio importante:** Como esto es un cambio en la estructura de la base de datos, ¡no olvides **detener el servidor y eliminar tu archivo `app.db`** (o `data.db`) antes de volver a correr `python run.py`!
