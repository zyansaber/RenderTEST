import os
from src.models import db
from src.models.user import User
from src.models.page import Page
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Handle DATABASE_URL and convert for SQLAlchemy if needed
    raw_db_url = os.environ.get("DATABASE_URL", "sqlite:///fallback.db")
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'temp'  # not used here

    db.init_app(app)
    return app

app = create_app()

with app.app_context():
    db.create_all()

    # Create default admin user if not exists
    admin = User.query.filter_by(username='zhihaiyan').first()
    if not admin:
        admin = User(username='zhihaiyan', email='zhihaiyan@example.com', is_admin=True)
        admin.set_password('abc')
        db.session.add(admin)

    db.session.commit()
    print("✅ Database tables created and admin user ensured.")
