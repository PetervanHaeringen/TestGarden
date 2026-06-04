# init_db.py
from app import create_app
from database.models import db

def init_db():
    app = create_app()
    with app.app_context():
        # Zorg dat alle modellen zijn geïmporteerd vóór create_all
        # (anders worden sommige tabellen niet aangemaakt)
        try:
            import users.models  # waar User staat
        except Exception as e:
            print("Kon users.models niet importeren:", e)

        db.create_all()
        print("✅ Database tabellen aangemaakt.")

if __name__ == "__main__":
    init_db()