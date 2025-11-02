from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import os

app = create_app()

def crear_admin():
    # --- ¡SOLUCIÓN! ---
    # 1. Usamos el 'contexto' de la app.
    # Esto le dice a 'db' a qué app de Flask pertenece.
    with app.app_context():
        # 2. Creamos todas las tablas (si no existen)
        db.create_all()

        username = 'admin'
        password = 'admin123' # ⚠️ Cambialo para producción

        # 3. Ahora esta consulta puede funcionar
        if User.query.filter_by(username=username).first():
            print("✅ El usuario admin ya existe.")
            return

        hashed_password = generate_password_hash(password)
        admin_user = User(username=username, password=hashed_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print(f"✅ Usuario '{username}' creado con contraseña '{password}' y permisos de admin.")

# Este bloque solo se ejecuta cuando corres `python run.py`
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    # 4. Llamamos a la función AQUÍ, justo antes de correr el servidor.
    crear_admin()

    # Ponemos debug=True para ver errores en el navegador
    # Render ignorará 'debug=True' en producción
    app.run(host='0.0.0.0', port=port, debug=True)


