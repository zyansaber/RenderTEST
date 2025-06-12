from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from src.models import db
from src.models.user import User
from src.models.page import Page
from src.models.permission import UserPagePermission
from functools import wraps

main_bp = Blueprint('main', __name__)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Home page
@main_bp.route('/')
@login_required
def index():
    return render_template('main/index.html')

# View PowerBI page
@main_bp.route('/page/<int:page_id>')
@login_required
def view_page(page_id):
    # 获取页面
    page = Page.query.get_or_404(page_id)

    # 权限检查
    user_id = session.get('user_id')
    is_admin = session.get('is_admin')

    if not is_admin:
        from src.models.permission import UserPagePermission
        permission = UserPagePermission.query.filter_by(
            user_id=user_id,
            page_id=page_id
        ).first()
        if not permission:
            flash('You do not have permission to view this page', 'danger')
            return redirect(url_for('main.index'))

    # 根据页面类型选择模板
    if page.type == 'custom':
        return render_template('pages/custom.html', page=page)
    else:
        return render_template('main/view_page.html', page=page)


# Get user's accessible pages for navigation
@main_bp.context_processor
def inject_user_pages():
    if not session.get('user_id'):
        return {'user_pages': []}
    
    user_id = session.get('user_id')
    is_admin = session.get('is_admin')
    
    if is_admin:
        # Admins can see all pages
        pages = Page.query.filter_by(is_active=True).order_by(Page.display_order).all()
    else:
        # Regular users can only see pages they have permission for
        permissions = UserPagePermission.query.filter_by(user_id=user_id).all()
        page_ids = [p.page_id for p in permissions]
        pages = Page.query.filter(Page.id.in_(page_ids), Page.is_active==True).order_by(Page.display_order).all()
    
    return {'user_pages': pages}
