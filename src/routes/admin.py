from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from src.models import db
from src.models.user import User
from src.models.page import Page
from src.models.permission import UserPagePermission
from functools import wraps
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login', next=request.url))
        if not session.get('is_admin'):
            flash('Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Admin dashboard
@admin_bp.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

# Page management
@admin_bp.route('/pages')
@admin_required
def list_pages():
    pages = Page.query.all()
    return render_template('admin/pages/list.html', pages=pages)

import os
from flask import request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from src.models.page import Page
from src.models import db

UPLOAD_FOLDER = 'static/uploads'

@admin_bp.route('/admin/pages/create', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        try:
            title = request.form['title']
            type = request.form.get('type', 'powerbi')
            description = request.form.get('description', '')
            link_url = request.form.get('link_url')
            link_text = request.form.get('link_text')
            powerbi_embed_url = request.form.get('powerbi_embed_url') if type == 'powerbi' else None
            display_order = int(request.form.get('display_order', 0))
            is_active = 'is_active' in request.form

            # 处理图片上传
            image_file = request.files.get('image_file')
            image_url = None
            if image_file and image_file.filename:
                filename = secure_filename(image_file.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                image_file.save(save_path)
                image_url = '/' + save_path.replace('\\\\', '/')

            page = Page(
                title=title,
                type=type,
                description=description,
                image_url=image_url,
                link_url=link_url,
                link_text=link_text,
                powerbi_embed_url=powerbi_embed_url,
                display_order=display_order,
                is_active=is_active
            )

            db.session.add(page)
            db.session.commit()
            flash('Page created successfully', 'success')
            return redirect(url_for('admin.list_pages'))

        except Exception as e:
            db.session.rollback()
            flash("Server error: " + str(e), "danger")
            print("CREATE PAGE ERROR:", e)
            return redirect(url_for('admin.create_page'))

    return render_template('admin/pages/create.html')



@admin_bp.route('/pages/<int:page_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_page(page_id):
    page = Page.query.get_or_404(page_id)
    
    if request.method == 'POST':
        page.title = request.form.get('title')
        page.description = request.form.get('description')
        page.powerbi_embed_url = request.form.get('powerbi_embed_url')
        page.display_order = request.form.get('display_order', 0)
        page.is_active = 'is_active' in request.form
        
        try:
            db.session.commit()  # Explicitly commit the transaction
            flash('Page updated successfully!', 'success')
            return redirect(url_for('admin.list_pages'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating page: {str(e)}', 'danger')
    
    return render_template('admin/pages/edit.html', page=page)

@admin_bp.route('/pages/<int:page_id>/delete', methods=['POST'])
@admin_required
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    
    try:
        db.session.delete(page)
        db.session.commit()  # Explicitly commit the transaction
        flash('Page deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting page: {str(e)}', 'danger')
    
    return redirect(url_for('admin.list_pages'))

# User management
@admin_bp.route('/users')
@admin_required
def list_users():
    users = User.query.all()
    return render_template('admin/users/list.html', users=users)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form
        is_active = 'is_active' in request.form
        
        user = User(
            username=username,
            email=email,
            is_admin=is_admin,
            is_active=is_active
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()  # Explicitly commit the transaction
            flash('User created successfully!', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'danger')
    
    return render_template('admin/users/create.html')

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        user.is_admin = 'is_admin' in request.form
        user.is_active = 'is_active' in request.form
        
        try:
            db.session.commit()  # Explicitly commit the transaction
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'danger')
    
    return render_template('admin/users/edit.html', user=user)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == session.get('user_id'):
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin.list_users'))
    
    try:
        db.session.delete(user)
        db.session.commit()  # Explicitly commit the transaction
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    
    return redirect(url_for('admin.list_users'))

# Permission management
@admin_bp.route('/permissions')
@admin_required
def list_permissions():
    permissions = UserPagePermission.query.all()
    return render_template('admin/permissions/list.html', permissions=permissions)

@admin_bp.route('/permissions/create', methods=['GET', 'POST'])
@admin_required
def create_permission():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        page_id = request.form.get('page_id')
        
        # Check if permission already exists
        existing = UserPagePermission.query.filter_by(
            user_id=user_id, 
            page_id=page_id
        ).first()
        
        if existing:
            flash('This permission already exists!', 'warning')
            return redirect(url_for('admin.list_permissions'))
        
        permission = UserPagePermission(
            user_id=user_id,
            page_id=page_id
        )
        
        try:
            db.session.add(permission)
            db.session.commit()  # Explicitly commit the transaction
            flash('Permission created successfully!', 'success')
            return redirect(url_for('admin.list_permissions'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating permission: {str(e)}', 'danger')
    
    users = User.query.filter_by(is_admin=False).all()
    pages = Page.query.all()
    return render_template('admin/permissions/create.html', users=users, pages=pages)

@admin_bp.route('/permissions/<int:permission_id>/delete', methods=['POST'])
@admin_required
def delete_permission(permission_id):
    permission = UserPagePermission.query.get_or_404(permission_id)
    
    try:
        db.session.delete(permission)
        db.session.commit()  # Explicitly commit the transaction
        flash('Permission deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting permission: {str(e)}', 'danger')
    
    return redirect(url_for('admin.list_permissions'))

@admin_bp.route('/users/<int:user_id>/permissions', methods=['GET', 'POST'])
@admin_required
def manage_user_permissions(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Get selected page IDs
        page_ids = request.form.getlist('page_ids')
        
        # Delete existing permissions
        UserPagePermission.query.filter_by(user_id=user.id).delete()
        
        # Add new permissions
        for page_id in page_ids:
            permission = UserPagePermission(user_id=user.id, page_id=page_id)
            db.session.add(permission)
        
        try:
            db.session.commit()  # Explicitly commit the transaction
            flash('User permissions updated successfully!', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating permissions: {str(e)}', 'danger')
    
    # Get all pages
    pages = Page.query.all()
    
    # Get user's current page permissions
    user_permissions = UserPagePermission.query.filter_by(user_id=user.id).all()
    user_page_ids = [p.page_id for p in user_permissions]
    
    return render_template('admin/users/permissions.html', 
                          user=user, 
                          pages=pages, 
                          user_page_ids=user_page_ids)
