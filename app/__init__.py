from app import create_app, db
from app.models import User

def crear_admin():
    username = "admin"
    email = "admin@example.com"
    password = "admin123"

    if User.query.filter_by(username=username).first():
        print("El usuario admin ya existe.")
        return

    admin = User(username=username, email=email)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print("Usuario admin creado correctamente.")

app = create_app()

if __name__ == "__main__":
    # Create admin inside app context
    with app.app_context():
        crear_admin()

    app.run(host="0.0.0.0", port=5000)
