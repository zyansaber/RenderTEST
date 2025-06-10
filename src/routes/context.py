from flask import Blueprint, g

context_bp = Blueprint('context', __name__)

@context_bp.app_context_processor
def inject_global_variables():
    return {
        'app_name': 'PowerBI Portal',
        'current_user': g.user if hasattr(g, 'user') else None
    }
