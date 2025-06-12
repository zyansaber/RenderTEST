from src.models import db

class Page(db.Model):
    __tablename__ = 'pages'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)  # 新增：HTML富文本内容
    image_url = db.Column(db.String(255))  # 新增：插图路径
    link_url = db.Column(db.String(255))  # 新增：链接地址
    link_text = db.Column(db.String(100))  # 新增：链接名称
    type = db.Column(db.String(50), default='powerbi')  # 新增：页面类型
    powerbi_embed_url = db.Column(db.String(500))  # 原字段
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Page {self.title}>'
