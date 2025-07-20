from . import db
from datetime import datetime
import uuid

class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    domain = db.Column(db.String(255))
    platform = db.Column(db.String(50), index=True)  # 'shopify', 'woocommerce', 'magento', etc.
    platform_store_id = db.Column(db.String(255))
    api_credentials = db.Column(db.JSON)  # Encrypted API keys and tokens
    status = db.Column(db.String(20), default='active', index=True)  # 'active', 'inactive', 'suspended'
    settings = db.Column(db.JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='store', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='store', lazy=True, cascade='all, delete-orphan')
    analytics_data = db.relationship('AnalyticsData', backref='store', lazy=True, cascade='all, delete-orphan')
    ad_campaigns = db.relationship('AdCampaign', backref='store', lazy=True)

    def __repr__(self):
        return f'<Store {self.name}>'

    @property
    def is_connected(self):
        """Check if store is connected to a platform"""
        return bool(self.platform and self.platform_store_id and self.api_credentials)

    @property
    def total_products(self):
        """Get total number of products"""
        return len(self.products)

    @property
    def total_orders(self):
        """Get total number of orders"""
        return len(self.orders)

    def to_dict(self, include_sensitive=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'domain': self.domain,
            'platform': self.platform,
            'status': self.status,
            'is_connected': self.is_connected,
            'total_products': self.total_products,
            'total_orders': self.total_orders,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'settings': self.settings or {}
        }
        
        if include_sensitive:
            data['platform_store_id'] = self.platform_store_id
            data['api_credentials'] = self.api_credentials
        
        return data

