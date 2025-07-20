from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    settings = db.Column(db.JSON, default=dict)
    
    # Relationships
    stores = db.relationship('Store', backref='owner', lazy=True, cascade='all, delete-orphan')
    payment_processors = db.relationship('PaymentProcessor', backref='user', lazy=True, cascade='all, delete-orphan')
    social_accounts = db.relationship('SocialMediaAccount', backref='user', lazy=True, cascade='all, delete-orphan')
    proxies = db.relationship('Proxy', backref='user', lazy=True, cascade='all, delete-orphan')
    research_data = db.relationship('MarketResearchData', backref='user', lazy=True, cascade='all, delete-orphan')
    ad_campaigns = db.relationship('AdCampaign', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.email

    def to_dict(self, include_sensitive=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'settings': self.settings or {}
        }
        
        if include_sensitive:
            data['stores_count'] = len(self.stores)
            data['payment_processors_count'] = len(self.payment_processors)
            data['social_accounts_count'] = len(self.social_accounts)
        
        return data
