import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, session, g
from src.models import db
from src.routes import auth_bp, main_bp, admin_bp, context_bp
from datetime import datetime
from src.models.user import User
from src.models.page import Page


def create_app():
    app = Flask(__name__)

    # Secret key
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_production')

    # Database connection
    raw_db_url = os.environ.get("DATABASE_URL", "sqlite:///fallback.db")
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB
    db.init_app(app)

    # Jinja global: current time
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}


    # Register blueprints
    app.register_blueprint(context_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Auto-initialize DB tables and default admin if needed
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='zhihaiyan').first():
            admin = User(username='zhihaiyan', email='zhihaiyan@example.com', is_admin=True)
            admin.set_password('abc')
            db.session.add(admin)
            db.session.commit()

    # Error pages
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
