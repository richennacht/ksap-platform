# KSAP Architecture Design Document

## 1. System Architecture Overview

KSAP follows a modern, scalable microservices architecture designed to handle the complex requirements of multi-store e-commerce management. The system is built with separation of concerns, ensuring each component can be developed, tested, and deployed independently while maintaining seamless integration.

### 1.1. High-Level Architecture

The KSAP platform consists of three primary layers:

1. **Presentation Layer**: React-based frontend application providing the user interface
2. **Application Layer**: Flask-based backend services handling business logic and API endpoints
3. **Data Layer**: PostgreSQL database with Redis for caching and session management

### 1.2. Microservices Architecture

The backend is organized into the following microservices:

- **User Management Service**: Authentication, authorization, user profiles
- **Store Management Service**: Store CRUD operations, multi-store orchestration
- **E-commerce Integration Service**: Shopify, WooCommerce, and other platform integrations
- **Order Management Service**: Order processing, fulfillment workflows
- **Payment Service**: Payment processor integrations and transaction management
- **Analytics Service**: Data aggregation, reporting, and insights
- **AI Service**: Integration with Gemini, GPT, and Claude for ad creation
- **Social Media Service**: Facebook/Instagram API integration and ad management
- **Proxy/VPN Service**: Network security and multi-account management
- **Market Research Service**: Competitor analysis and trend monitoring



## 2. API Design and Endpoints

The KSAP backend exposes a comprehensive RESTful API that follows industry best practices for resource naming, HTTP methods, and response formats.

### 2.1. API Structure

All API endpoints follow the pattern: `/api/v1/{resource}`

#### Authentication Endpoints
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/refresh` - Token refresh
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/forgot-password` - Password reset request
- `POST /api/v1/auth/reset-password` - Password reset confirmation

#### User Management Endpoints
- `GET /api/v1/users/profile` - Get current user profile
- `PUT /api/v1/users/profile` - Update user profile
- `POST /api/v1/users/change-password` - Change password
- `GET /api/v1/users/settings` - Get user settings
- `PUT /api/v1/users/settings` - Update user settings

#### Store Management Endpoints
- `GET /api/v1/stores` - List all user stores
- `POST /api/v1/stores` - Create new store
- `GET /api/v1/stores/{store_id}` - Get store details
- `PUT /api/v1/stores/{store_id}` - Update store
- `DELETE /api/v1/stores/{store_id}` - Delete store
- `POST /api/v1/stores/{store_id}/connect` - Connect to e-commerce platform

#### Product Management Endpoints
- `GET /api/v1/stores/{store_id}/products` - List store products
- `POST /api/v1/stores/{store_id}/products` - Create product
- `GET /api/v1/stores/{store_id}/products/{product_id}` - Get product details
- `PUT /api/v1/stores/{store_id}/products/{product_id}` - Update product
- `DELETE /api/v1/stores/{store_id}/products/{product_id}` - Delete product
- `POST /api/v1/stores/{store_id}/products/bulk-update` - Bulk product operations

#### Order Management Endpoints
- `GET /api/v1/stores/{store_id}/orders` - List store orders
- `GET /api/v1/orders` - List all orders across stores
- `GET /api/v1/orders/{order_id}` - Get order details
- `PUT /api/v1/orders/{order_id}/status` - Update order status
- `POST /api/v1/orders/{order_id}/fulfill` - Fulfill order
- `POST /api/v1/orders/{order_id}/ship` - Ship order
- `GET /api/v1/orders/{order_id}/tracking` - Get tracking information

#### Payment Management Endpoints
- `GET /api/v1/payment-processors` - List connected payment processors
- `POST /api/v1/payment-processors` - Connect payment processor
- `GET /api/v1/payment-processors/{processor_id}` - Get processor details
- `PUT /api/v1/payment-processors/{processor_id}` - Update processor settings
- `DELETE /api/v1/payment-processors/{processor_id}` - Disconnect processor
- `GET /api/v1/payment-processors/{processor_id}/transactions` - List transactions
- `GET /api/v1/payment-processors/{processor_id}/payouts` - List payouts

#### Analytics Endpoints
- `GET /api/v1/analytics/dashboard` - Get dashboard data
- `GET /api/v1/analytics/sales` - Sales analytics
- `GET /api/v1/analytics/traffic` - Traffic analytics
- `GET /api/v1/analytics/customers` - Customer analytics
- `GET /api/v1/analytics/products` - Product performance analytics
- `GET /api/v1/analytics/marketing` - Marketing analytics
- `POST /api/v1/analytics/reports` - Generate custom reports

#### AI Services Endpoints
- `POST /api/v1/ai/research` - Market research using Gemini
- `POST /api/v1/ai/generate-image` - Generate ad images using GPT
- `POST /api/v1/ai/generate-copy` - Generate ad copy using Claude
- `POST /api/v1/ai/create-campaign` - Full AI campaign creation
- `GET /api/v1/ai/campaigns` - List AI-generated campaigns
- `GET /api/v1/ai/campaigns/{campaign_id}` - Get campaign details

#### Social Media Management Endpoints
- `GET /api/v1/social/accounts` - List social media accounts
- `POST /api/v1/social/accounts` - Add social media account
- `GET /api/v1/social/accounts/{account_id}` - Get account details
- `PUT /api/v1/social/accounts/{account_id}` - Update account
- `DELETE /api/v1/social/accounts/{account_id}` - Remove account
- `GET /api/v1/social/campaigns` - List ad campaigns
- `POST /api/v1/social/campaigns` - Create ad campaign
- `GET /api/v1/social/campaigns/{campaign_id}` - Get campaign details
- `PUT /api/v1/social/campaigns/{campaign_id}` - Update campaign
- `DELETE /api/v1/social/campaigns/{campaign_id}` - Delete campaign

#### Market Research Endpoints
- `GET /api/v1/research/competitors` - List tracked competitors
- `POST /api/v1/research/competitors` - Add competitor
- `GET /api/v1/research/competitors/{competitor_id}/ads` - Get competitor ads
- `GET /api/v1/research/trends` - Get market trends
- `POST /api/v1/research/analyze` - Analyze market data
- `GET /api/v1/research/reports` - List research reports

#### VPN/Proxy Management Endpoints
- `GET /api/v1/proxies` - List configured proxies
- `POST /api/v1/proxies` - Add proxy configuration
- `GET /api/v1/proxies/{proxy_id}` - Get proxy details
- `PUT /api/v1/proxies/{proxy_id}` - Update proxy
- `DELETE /api/v1/proxies/{proxy_id}` - Remove proxy
- `POST /api/v1/proxies/{proxy_id}/test` - Test proxy connection

### 2.2. Response Format Standards

All API responses follow a consistent format:

```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_123456789"
}
```

Error responses:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "req_123456789"
}
```



## 3. Database Schema Design

The KSAP database is designed using PostgreSQL with a normalized schema that supports complex relationships while maintaining performance and data integrity.

### 3.1. Core Entities

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    settings JSONB DEFAULT '{}'
);
```

#### Stores Table
```sql
CREATE TABLE stores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    domain VARCHAR(255),
    platform VARCHAR(50), -- 'shopify', 'woocommerce', 'magento', etc.
    platform_store_id VARCHAR(255),
    api_credentials JSONB, -- Encrypted API keys and tokens
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'suspended'
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Products Table
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_id UUID NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    platform_product_id VARCHAR(255),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    compare_at_price DECIMAL(10,2),
    cost_per_item DECIMAL(10,2),
    sku VARCHAR(255),
    barcode VARCHAR(255),
    inventory_quantity INTEGER DEFAULT 0,
    track_inventory BOOLEAN DEFAULT true,
    weight DECIMAL(8,2),
    images JSONB DEFAULT '[]',
    tags JSONB DEFAULT '[]',
    vendor VARCHAR(255),
    product_type VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Orders Table
```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_id UUID NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    platform_order_id VARCHAR(255),
    order_number VARCHAR(100),
    customer_email VARCHAR(255),
    customer_name VARCHAR(255),
    customer_phone VARCHAR(50),
    billing_address JSONB,
    shipping_address JSONB,
    subtotal DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    shipping_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(50), -- 'pending', 'paid', 'fulfilled', 'shipped', 'delivered', 'cancelled'
    fulfillment_status VARCHAR(50),
    payment_status VARCHAR(50),
    notes TEXT,
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Order Items Table
```sql
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    platform_product_id VARCHAR(255),
    title VARCHAR(500),
    sku VARCHAR(255),
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    variant_title VARCHAR(255),
    properties JSONB DEFAULT '{}'
);
```

#### Payment Processors Table
```sql
CREATE TABLE payment_processors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL, -- 'stripe', 'paypal', 'square', etc.
    api_credentials JSONB, -- Encrypted API keys
    webhook_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Transactions Table
```sql
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_processor_id UUID NOT NULL REFERENCES payment_processors(id),
    order_id UUID REFERENCES orders(id),
    platform_transaction_id VARCHAR(255),
    type VARCHAR(50), -- 'payment', 'refund', 'chargeback', 'fee'
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(50), -- 'pending', 'completed', 'failed', 'cancelled'
    gateway_response JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Social Media Accounts Table
```sql
CREATE TABLE social_media_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- 'facebook', 'instagram', 'tiktok', etc.
    account_name VARCHAR(255),
    account_id VARCHAR(255),
    access_token TEXT, -- Encrypted
    refresh_token TEXT, -- Encrypted
    token_expires_at TIMESTAMP WITH TIME ZONE,
    proxy_id UUID REFERENCES proxies(id),
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'suspended', 'banned'
    warmup_status VARCHAR(50), -- 'new', 'warming', 'ready', 'flagged'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Ad Campaigns Table
```sql
CREATE TABLE ad_campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    store_id UUID REFERENCES stores(id),
    social_account_id UUID REFERENCES social_media_accounts(id),
    name VARCHAR(255) NOT NULL,
    objective VARCHAR(100), -- 'traffic', 'conversions', 'brand_awareness', etc.
    status VARCHAR(50), -- 'draft', 'active', 'paused', 'completed'
    budget_type VARCHAR(20), -- 'daily', 'lifetime'
    budget_amount DECIMAL(10,2),
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    target_audience JSONB,
    creatives JSONB, -- Array of creative assets
    platform_campaign_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Proxies Table
```sql
CREATE TABLE proxies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255),
    host VARCHAR(255) NOT NULL,
    port INTEGER NOT NULL,
    username VARCHAR(255),
    password VARCHAR(255), -- Encrypted
    protocol VARCHAR(10) DEFAULT 'http', -- 'http', 'https', 'socks5'
    country VARCHAR(2),
    is_active BOOLEAN DEFAULT true,
    last_tested TIMESTAMP WITH TIME ZONE,
    test_result VARCHAR(20), -- 'success', 'failed', 'timeout'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Market Research Data Table
```sql
CREATE TABLE market_research_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    research_type VARCHAR(50), -- 'competitor_ad', 'trend_analysis', 'product_research'
    query_parameters JSONB,
    data JSONB NOT NULL,
    source VARCHAR(100), -- 'facebook_ad_library', 'google_trends', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Analytics Data Table
```sql
CREATE TABLE analytics_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_id UUID NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    metric_type VARCHAR(100), -- 'sales', 'traffic', 'conversion', etc.
    metric_name VARCHAR(100),
    value DECIMAL(15,4),
    dimensions JSONB, -- Additional dimensions like date, product_id, etc.
    date_recorded DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2. Indexes and Performance Optimization

```sql
-- User indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Store indexes
CREATE INDEX idx_stores_user_id ON stores(user_id);
CREATE INDEX idx_stores_platform ON stores(platform);
CREATE INDEX idx_stores_status ON stores(status);

-- Product indexes
CREATE INDEX idx_products_store_id ON products(store_id);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_status ON products(status);

-- Order indexes
CREATE INDEX idx_orders_store_id ON orders(store_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_customer_email ON orders(customer_email);

-- Transaction indexes
CREATE INDEX idx_transactions_payment_processor_id ON transactions(payment_processor_id);
CREATE INDEX idx_transactions_order_id ON transactions(order_id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);

-- Analytics indexes
CREATE INDEX idx_analytics_store_id ON analytics_data(store_id);
CREATE INDEX idx_analytics_metric_type ON analytics_data(metric_type);
CREATE INDEX idx_analytics_date_recorded ON analytics_data(date_recorded);
```

### 3.3. Data Relationships

The database schema maintains referential integrity through foreign key constraints while allowing for flexible data storage using JSONB columns for configuration and metadata. Key relationships include:

- Users can have multiple Stores (1:N)
- Stores can have multiple Products and Orders (1:N)
- Orders can have multiple Order Items (1:N)
- Users can have multiple Payment Processors and Social Media Accounts (1:N)
- Social Media Accounts can be associated with Proxies (N:1)
- Ad Campaigns belong to Users and can be associated with Stores and Social Accounts (N:1)

