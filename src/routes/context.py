from flask import Blueprint, g
from src.models.page import Page
from src.models.permission import UserPagePermission

context_bp = Blueprint('context', __name__)

@context_bp.app_context_processor
def inject_global_variables():
    if hasattr(g, 'user') and g.user:
        accessible_pages = [p.page for p in g.user.page_permissions]
        accessible_pages = sorted(accessible_pages, key=lambda x: x.display_order)
    else:
        accessible_pages = []

    return {
        'app_name': 'PowerBI Portal',
        'current_user': g.user if hasattr(g, 'user') else None,
        'accessible_pages': accessible_pages
    }
