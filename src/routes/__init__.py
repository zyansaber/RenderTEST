from src.routes.auth import auth_bp
from src.routes.main import main_bp
from src.routes.admin import admin_bp
from src.routes.context import context_bp

# Export all blueprints
__all__ = ['auth_bp', 'main_bp', 'admin_bp', 'context_bp']
