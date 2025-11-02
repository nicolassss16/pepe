from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import os

app = create_app()

def crear_admin():
    # Usamos el contexto de la aplicación
    with app.app_context():
        # --- BUENA PRÁCTICA ---
        # Asegura que todas las tablas existan ANTES de crear el admin
        db.create_all()
        # --------------------

        username = 'admin'
        password = 'admin123' # ⚠️ Cambialo para producción

        if User.query.filter_by(username=username).first():
            print("✅ El usuario admin ya existe.")
            return

        hashed_password = generate_password_hash(password)
        
        # --- CAMBIO IMPORTANTE ---
        # Le damos el permiso de admin al crearlo
        admin_user = User(username=username, password=hashed_password, is_admin=True)
        # ------------------------
        
        db.session.add(admin_user)
        db.session.commit()
        print(f"✅ Usuario '{username}' creado con contraseña '{password}' y permisos de admin.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Llama a la función ANTES de correr la app
    crear_admin()

    # Ponemos debug=True para ver errores en el navegador
    app.run(host='0.0.0.0', port=port, debug=True)
