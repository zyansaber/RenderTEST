from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from functools import wraps
from src.models import db
from src.models.user import User
from src.models.page import Page
from src.models.permission import UserPagePermission

main_bp = Blueprint('main', __name__)

# 登录保护装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# 首页
@main_bp.route('/')
@login_required
def index():
    return render_template('main/index.html')


# 访问页面（PowerBI / Custom）
@main_bp.route('/page/<int:page_id>')
@login_required
def view_page(page_id):
    page = Page.query.get_or_404(page_id)

    user_id = session.get('user_id')
    is_admin = session.get('is_admin', False)

    # 如果不是管理员，检查权限
    if not is_admin:
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


# 页面导航显示当前用户能看到的页面
@main_bp.context_processor
def inject_user_pages():
    if not session.get('user_id'):
        return {'accessible_pages': []}

    user_id = session.get('user_id')
    is_admin = session.get('is_admin', False)

    if is_admin:
        pages = Page.query.filter_by(is_active=True).order_by(Page.display_order).all()
    else:
        permissions = UserPagePermission.query.filter_by(user_id=user_id).all()
        page_ids = [p.page_id for p in permissions]
        pages = Page.query.filter(Page.id.in_(page_ids), Page.is_active == True).order_by(Page.display_order).all()

    return {'accessible_pages': pages}
