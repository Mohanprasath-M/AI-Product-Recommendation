-- =====================================================================
-- AI PRODUCT RECOMMENDATION & CUSTOMER INTELLIGENCE PLATFORM
-- PRODUCTION MYSQL DATABASE SCHEMA (OPTIMIZED FOR MYSQL WORKBENCH)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS ai_recommendation_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ai_recommendation_db;

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'CUSTOMER',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. CUSTOMER SEGMENTS TABLE
CREATE TABLE IF NOT EXISTS customer_segments (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    cluster_index INT NOT NULL UNIQUE,
    description TEXT,
    customer_count INT DEFAULT 0,
    avg_spending FLOAT DEFAULT 0.0,
    avg_order_value FLOAT DEFAULT 0.0,
    avg_purchase_frequency FLOAT DEFAULT 0.0,
    avg_churn_risk FLOAT DEFAULT 0.0,
    key_characteristics JSON,
    cluster_center JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_segments_cluster (cluster_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. CUSTOMERS TABLE
CREATE TABLE IF NOT EXISTS customers (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NULL,
    customer_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NULL,
    age INT NULL,
    gender VARCHAR(20) NULL,
    location VARCHAR(100) NULL,
    persona VARCHAR(100) DEFAULT 'General Shopper',
    total_spend FLOAT DEFAULT 0.0,
    total_orders INT DEFAULT 0,
    avg_order_value FLOAT DEFAULT 0.0,
    clv_historical FLOAT DEFAULT 0.0,
    clv_estimated FLOAT DEFAULT 0.0,
    churn_risk_score FLOAT DEFAULT 0.0,
    churn_risk_level VARCHAR(20) DEFAULT 'LOW',
    segment_id VARCHAR(36) NULL,
    favorite_category VARCHAR(100) NULL,
    favorite_brand VARCHAR(100) NULL,
    preferred_price_min FLOAT DEFAULT 0.0,
    preferred_price_max FLOAT DEFAULT 1000.0,
    last_active_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customers_email (email),
    INDEX idx_customers_code (customer_code),
    INDEX idx_customers_segment (segment_id),
    INDEX idx_customers_churn (churn_risk_level),
    CONSTRAINT fk_customers_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_customers_segment FOREIGN KEY (segment_id) REFERENCES customer_segments(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. CATEGORIES TABLE
CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50) DEFAULT 'Tag',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_categories_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. BRANDS TABLE
CREATE TABLE IF NOT EXISTS brands (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    logo_url VARCHAR(255) NULL,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_brands_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. PRODUCTS TABLE
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(36) PRIMARY KEY,
    product_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100) NULL,
    category_id VARCHAR(36) NULL,
    brand VARCHAR(100) NOT NULL,
    brand_id VARCHAR(36) NULL,
    price FLOAT NOT NULL,
    discount FLOAT DEFAULT 0.0,
    stock INT DEFAULT 100,
    rating FLOAT DEFAULT 0.0,
    rating_count INT DEFAULT 0,
    image_url VARCHAR(500) NULL,
    tags VARCHAR(500) DEFAULT '',
    specifications JSON,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    views_count INT DEFAULT 0,
    clicks_count INT DEFAULT 0,
    cart_adds_count INT DEFAULT 0,
    wishlist_adds_count INT DEFAULT 0,
    purchases_count INT DEFAULT 0,
    revenue_generated FLOAT DEFAULT 0.0,
    popularity_score FLOAT DEFAULT 0.0,
    trend_score FLOAT DEFAULT 0.0,
    trend_status VARCHAR(20) DEFAULT 'STABLE',
    sentiment_score FLOAT DEFAULT 0.0,
    positive_sentiment_pct FLOAT DEFAULT 0.0,
    neutral_sentiment_pct FLOAT DEFAULT 0.0,
    negative_sentiment_pct FLOAT DEFAULT 0.0,
    top_positive_topics JSON,
    top_negative_topics JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_products_category (category),
    INDEX idx_products_brand (brand),
    INDEX idx_products_price (price),
    INDEX idx_products_rating (rating),
    INDEX idx_products_status (status),
    CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    CONSTRAINT fk_products_brand FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. INTERACTIONS TABLE
CREATE TABLE IF NOT EXISTS interactions (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    weight FLOAT DEFAULT 1.0,
    session_id VARCHAR(100) NULL,
    metadata_json JSON,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_interactions_customer (customer_id),
    INDEX idx_interactions_product (product_id),
    INDEX idx_interactions_event (event_type),
    INDEX idx_interactions_timestamp (timestamp),
    CONSTRAINT fk_interactions_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    CONSTRAINT fk_interactions_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. ORDERS & ORDER ITEMS TABLE
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(36) PRIMARY KEY,
    order_code VARCHAR(50) NOT NULL UNIQUE,
    customer_id VARCHAR(36) NOT NULL,
    total_amount FLOAT NOT NULL,
    discount_amount FLOAT DEFAULT 0.0,
    tax_amount FLOAT DEFAULT 0.0,
    final_amount FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'COMPLETED',
    payment_method VARCHAR(50) DEFAULT 'CREDIT_CARD',
    shipping_address TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_orders_customer (customer_id),
    INDEX idx_orders_created (created_at),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS order_items (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INT DEFAULT 1,
    unit_price FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    INDEX idx_order_items_order (order_id),
    INDEX idx_order_items_product (product_id),
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. REVIEWS TABLE
CREATE TABLE IF NOT EXISTS reviews (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    rating FLOAT NOT NULL,
    title VARCHAR(255) NULL,
    comment TEXT NOT NULL,
    sentiment_label VARCHAR(20) DEFAULT 'NEUTRAL',
    sentiment_score FLOAT DEFAULT 0.0,
    positive_topics JSON,
    negative_topics JSON,
    verified_purchase INT DEFAULT 1,
    helpful_votes INT DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_reviews_product (product_id),
    INDEX idx_reviews_customer (customer_id),
    INDEX idx_reviews_sentiment (sentiment_label),
    CONSTRAINT fk_reviews_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    CONSTRAINT fk_reviews_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. ML MODEL VERSIONS & METRICS
CREATE TABLE IF NOT EXISTS model_versions (
    id VARCHAR(36) PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    algorithm VARCHAR(100) NOT NULL,
    hyperparameters JSON,
    metrics JSON,
    is_active BOOLEAN DEFAULT FALSE,
    artifact_path VARCHAR(255) NULL,
    dataset_size INT DEFAULT 0,
    training_duration_seconds FLOAT DEFAULT 0.0,
    trained_by VARCHAR(100) DEFAULT 'SYSTEM',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_model_name (model_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. RECOMMENDATION EVENTS
CREATE TABLE IF NOT EXISTS recommendation_events (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    model_version VARCHAR(50) DEFAULT 'v1.0',
    recommendation_type VARCHAR(50) DEFAULT 'HYBRID',
    score FLOAT DEFAULT 0.0,
    rank INT DEFAULT 1,
    clicked BOOLEAN DEFAULT FALSE,
    added_to_cart BOOLEAN DEFAULT FALSE,
    purchased BOOLEAN DEFAULT FALSE,
    experiment_group VARCHAR(20) DEFAULT 'A',
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rec_events_customer (customer_id),
    INDEX idx_rec_events_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. SEARCH EVENTS
CREATE TABLE IF NOT EXISTS search_events (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NULL,
    query VARCHAR(255) NOT NULL,
    result_count INT DEFAULT 0,
    clicked_product_id VARCHAR(36) NULL,
    purchased_product_id VARCHAR(36) NULL,
    session_id VARCHAR(100) NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_search_query (query),
    INDEX idx_search_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
