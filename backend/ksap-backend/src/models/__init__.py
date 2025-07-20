from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

# Import all models
from .user import User
from .store import Store
from .product import Product
from .order import Order, OrderItem
from .payment import PaymentProcessor, Transaction
from .social import SocialMediaAccount, AdCampaign
from .proxy import Proxy
from .analytics import AnalyticsData
from .research import MarketResearchData

__all__ = [
    'db',
    'User',
    'Store', 
    'Product',
    'Order',
    'OrderItem',
    'PaymentProcessor',
    'Transaction',
    'SocialMediaAccount',
    'AdCampaign',
    'Proxy',
    'AnalyticsData',
    'MarketResearchData'
]

