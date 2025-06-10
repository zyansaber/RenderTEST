from src.models import db

class UserPagePermission(db.Model):
    __tablename__ = 'user_page_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Define relationships
    user = db.relationship('User', backref=db.backref('page_permissions', cascade='all, delete-orphan'))
    page = db.relationship('Page', backref=db.backref('user_permissions', cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<UserPagePermission user_id={self.user_id} page_id={self.page_id}>'
