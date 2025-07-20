"""
Supabase database schema definitions for KSAP platform
These are the SQL commands to create tables in Supabase
"""

# Users table (extends Supabase auth.users)
USERS_TABLE = """
CREATE TABLE IF NOT EXISTS public.users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    settings JSONB DEFAULT '{}'::jsonb
);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON public.users(created_at);
"""

# Stores table
STORES_TABLE = """
CREATE TABLE IF NOT EXISTS public.stores (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    domain VARCHAR(255),
    platform VARCHAR(50), -- 'shopify', 'woocommerce', 'magento', etc.
    platform_store_id VARCHAR(255),
    api_credentials JSONB, -- Encrypted API keys and tokens
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'suspended'
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE public.stores ENABLE ROW LEVEL SECURITY;

-- Users can only see their own stores
CREATE POLICY "Users can view own stores" ON public.stores
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own stores" ON public.stores
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own stores" ON public.stores
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own stores" ON public.stores
    FOR DELETE USING (auth.uid() = user_id);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_stores_user_id ON public.stores(user_id);
CREATE INDEX IF NOT EXISTS idx_stores_platform ON public.stores(platform);
CREATE INDEX IF NOT EXISTS idx_stores_status ON public.stores(status);
"""

# Products table
PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS public.products (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    store_id UUID REFERENCES public.stores(id) ON DELETE CASCADE NOT NULL,
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
    images JSONB DEFAULT '[]'::jsonb,
    tags JSONB DEFAULT '[]'::jsonb,
    vendor VARCHAR(255),
    product_type VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

-- Users can only see products from their own stores
CREATE POLICY "Users can view own store products" ON public.products
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = products.store_id 
            AND stores.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert products to own stores" ON public.products
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = products.store_id 
            AND stores.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update own store products" ON public.products
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = products.store_id 
            AND stores.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete own store products" ON public.products
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = products.store_id 
            AND stores.user_id = auth.uid()
        )
    );

-- Indexes
CREATE INDEX IF NOT EXISTS idx_products_store_id ON public.products(store_id);
CREATE INDEX IF NOT EXISTS idx_products_sku ON public.products(sku);
CREATE INDEX IF NOT EXISTS idx_products_status ON public.products(status);
"""

# Orders table
ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS public.orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    store_id UUID REFERENCES public.stores(id) ON DELETE CASCADE NOT NULL,
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
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

-- Users can only see orders from their own stores
CREATE POLICY "Users can view own store orders" ON public.orders
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = orders.store_id 
            AND stores.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert orders to own stores" ON public.orders
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = orders.store_id 
            AND stores.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update own store orders" ON public.orders
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = orders.store_id 
            AND stores.user_id = auth.uid()
        )
    );

-- Indexes
CREATE INDEX IF NOT EXISTS idx_orders_store_id ON public.orders(store_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON public.orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON public.orders(created_at);
CREATE INDEX IF NOT EXISTS idx_orders_customer_email ON public.orders(customer_email);
"""

# Order Items table
ORDER_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS public.order_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_id UUID REFERENCES public.orders(id) ON DELETE CASCADE NOT NULL,
    product_id UUID REFERENCES public.products(id),
    platform_product_id VARCHAR(255),
    title VARCHAR(500),
    sku VARCHAR(255),
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    variant_title VARCHAR(255),
    properties JSONB DEFAULT '{}'::jsonb
);

-- Enable RLS
ALTER TABLE public.order_items ENABLE ROW LEVEL SECURITY;

-- Users can only see order items from their own store orders
CREATE POLICY "Users can view own store order items" ON public.order_items
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.orders 
            JOIN public.stores ON stores.id = orders.store_id
            WHERE orders.id = order_items.order_id 
            AND stores.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert order items to own store orders" ON public.order_items
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.orders 
            JOIN public.stores ON stores.id = orders.store_id
            WHERE orders.id = order_items.order_id 
            AND stores.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update own store order items" ON public.order_items
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.orders 
            JOIN public.stores ON stores.id = orders.store_id
            WHERE orders.id = order_items.order_id 
            AND stores.user_id = auth.uid()
        )
    );
"""

# Payment Processors table
PAYMENT_PROCESSORS_TABLE = """
CREATE TABLE IF NOT EXISTS public.payment_processors (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    name VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL, -- 'stripe', 'paypal', 'square', etc.
    api_credentials JSONB, -- Encrypted API keys
    webhook_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE public.payment_processors ENABLE ROW LEVEL SECURITY;

-- Users can only see their own payment processors
CREATE POLICY "Users can view own payment processors" ON public.payment_processors
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own payment processors" ON public.payment_processors
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own payment processors" ON public.payment_processors
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own payment processors" ON public.payment_processors
    FOR DELETE USING (auth.uid() = user_id);
"""

# Social Media Accounts table
SOCIAL_MEDIA_ACCOUNTS_TABLE = """
CREATE TABLE IF NOT EXISTS public.social_media_accounts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    platform VARCHAR(50) NOT NULL, -- 'facebook', 'instagram', 'tiktok', etc.
    account_name VARCHAR(255),
    account_id VARCHAR(255),
    access_token TEXT, -- Encrypted
    refresh_token TEXT, -- Encrypted
    token_expires_at TIMESTAMP WITH TIME ZONE,
    proxy_id UUID REFERENCES public.proxies(id),
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'suspended', 'banned'
    warmup_status VARCHAR(50), -- 'new', 'warming', 'ready', 'flagged'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE public.social_media_accounts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own social media accounts
CREATE POLICY "Users can view own social accounts" ON public.social_media_accounts
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own social accounts" ON public.social_media_accounts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own social accounts" ON public.social_media_accounts
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own social accounts" ON public.social_media_accounts
    FOR DELETE USING (auth.uid() = user_id);
"""

# Proxies table
PROXIES_TABLE = """
CREATE TABLE IF NOT EXISTS public.proxies (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
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

-- Enable RLS
ALTER TABLE public.proxies ENABLE ROW LEVEL SECURITY;

-- Users can only see their own proxies
CREATE POLICY "Users can view own proxies" ON public.proxies
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own proxies" ON public.proxies
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own proxies" ON public.proxies
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own proxies" ON public.proxies
    FOR DELETE USING (auth.uid() = user_id);
"""

# Ad Campaigns table
AD_CAMPAIGNS_TABLE = """
CREATE TABLE IF NOT EXISTS public.ad_campaigns (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    store_id UUID REFERENCES public.stores(id),
    social_account_id UUID REFERENCES public.social_media_accounts(id),
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

-- Enable RLS
ALTER TABLE public.ad_campaigns ENABLE ROW LEVEL SECURITY;

-- Users can only see their own ad campaigns
CREATE POLICY "Users can view own ad campaigns" ON public.ad_campaigns
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own ad campaigns" ON public.ad_campaigns
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own ad campaigns" ON public.ad_campaigns
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own ad campaigns" ON public.ad_campaigns
    FOR DELETE USING (auth.uid() = user_id);
"""

# Analytics Data table
ANALYTICS_DATA_TABLE = """
CREATE TABLE IF NOT EXISTS public.analytics_data (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    store_id UUID REFERENCES public.stores(id) ON DELETE CASCADE NOT NULL,
    metric_type VARCHAR(100), -- 'sales', 'traffic', 'conversion', etc.
    metric_name VARCHAR(100),
    value DECIMAL(15,4),
    dimensions JSONB, -- Additional dimensions like date, product_id, etc.
    date_recorded DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE public.analytics_data ENABLE ROW LEVEL SECURITY;

-- Users can only see analytics from their own stores
CREATE POLICY "Users can view own store analytics" ON public.analytics_data
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = analytics_data.store_id 
            AND stores.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert analytics to own stores" ON public.analytics_data
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.stores 
            WHERE stores.id = analytics_data.store_id 
            AND stores.user_id = auth.uid()
        )
    );

-- Indexes
CREATE INDEX IF NOT EXISTS idx_analytics_store_id ON public.analytics_data(store_id);
CREATE INDEX IF NOT EXISTS idx_analytics_metric_type ON public.analytics_data(metric_type);
CREATE INDEX IF NOT EXISTS idx_analytics_date_recorded ON public.analytics_data(date_recorded);
"""

# Market Research Data table
MARKET_RESEARCH_DATA_TABLE = """
CREATE TABLE IF NOT EXISTS public.market_research_data (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    research_type VARCHAR(50), -- 'competitor_ad', 'trend_analysis', 'product_research'
    query_parameters JSONB,
    data JSONB NOT NULL,
    source VARCHAR(100), -- 'facebook_ad_library', 'google_trends', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE public.market_research_data ENABLE ROW LEVEL SECURITY;

-- Users can only see their own research data
CREATE POLICY "Users can view own research data" ON public.market_research_data
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own research data" ON public.market_research_data
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own research data" ON public.market_research_data
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own research data" ON public.market_research_data
    FOR DELETE USING (auth.uid() = user_id);
"""

# Function to handle updated_at timestamps
UPDATED_AT_FUNCTION = """
CREATE OR REPLACE FUNCTION handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

# Triggers for updated_at
UPDATED_AT_TRIGGERS = """
-- Users trigger
CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION handle_updated_at();

-- Stores trigger
CREATE TRIGGER trigger_stores_updated_at
    BEFORE UPDATE ON public.stores
    FOR EACH ROW EXECUTE FUNCTION handle_updated_at();

-- Products trigger
CREATE TRIGGER trigger_products_updated_at
    BEFORE UPDATE ON public.products
    FOR EACH ROW EXECUTE FUNCTION handle_updated_at();

-- Orders trigger
CREATE TRIGGER trigger_orders_updated_at
    BEFORE UPDATE ON public.orders
    FOR EACH ROW EXECUTE FUNCTION handle_updated_at();

-- Payment Processors trigger
CREATE TRIGGER trigger_payment_processors_updated_at
    BEFORE UPDATE ON public.payment_processors
    FOR EACH ROW EXECUTE FUNCTION handle_updated_at();

-- Social Media Accounts trigger
CREATE TRIGGER trigger_social_media_accounts_updated_at
    BEFORE UPDATE ON public.social_media_accounts
    FOR EACH ROW EXECUTE FUNCTION handle_updated_at();

-- Ad Campaigns trigger
CREATE TRIGGER trigger_ad_campaigns_updated_at
    BEFORE UPDATE ON public.ad_campaigns
    FOR EACH ROW EXECUTE FUNCTION handle_updated_at();
"""

# All table creation commands in order
ALL_TABLES = [
    USERS_TABLE,
    STORES_TABLE,
    PRODUCTS_TABLE,
    ORDERS_TABLE,
    ORDER_ITEMS_TABLE,
    PAYMENT_PROCESSORS_TABLE,
    PROXIES_TABLE,
    SOCIAL_MEDIA_ACCOUNTS_TABLE,
    AD_CAMPAIGNS_TABLE,
    ANALYTICS_DATA_TABLE,
    MARKET_RESEARCH_DATA_TABLE,
    UPDATED_AT_FUNCTION,
    UPDATED_AT_TRIGGERS
]

def create_tables(supabase_client):
    """Create all tables in Supabase"""
    for table_sql in ALL_TABLES:
        try:
            supabase_client.rpc('exec_sql', {'sql': table_sql}).execute()
            print(f"Successfully executed SQL block")
        except Exception as e:
            print(f"Error executing SQL: {e}")
            print(f"SQL: {table_sql[:100]}...")

def drop_tables(supabase_client):
    """Drop all tables (for development/testing)"""
    tables = [
        'market_research_data',
        'analytics_data', 
        'ad_campaigns',
        'social_media_accounts',
        'proxies',
        'payment_processors',
        'order_items',
        'orders',
        'products',
        'stores',
        'users'
    ]
    
    for table in tables:
        try:
            supabase_client.rpc('exec_sql', {'sql': f'DROP TABLE IF EXISTS public.{table} CASCADE;'}).execute()
            print(f"Dropped table: {table}")
        except Exception as e:
            print(f"Error dropping table {table}: {e}")

