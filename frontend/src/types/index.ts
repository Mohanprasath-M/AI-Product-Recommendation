export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'ADMIN' | 'ANALYST' | 'CUSTOMER';
  customer_id?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  role: string;
  user_id: string;
  customer_id?: string;
  email: string;
  name: string;
}

export interface Product {
  id: string;
  product_code: string;
  name: string;
  description: string;
  category: string;
  subcategory?: string;
  brand: string;
  price: number;
  discount: number;
  stock: number;
  rating: number;
  rating_count: number;
  image_url?: string;
  tags?: string;
  specifications?: Record<string, any>;
  status: string;
  views_count: number;
  clicks_count: number;
  cart_adds_count: number;
  wishlist_adds_count: number;
  purchases_count: number;
  revenue_generated: number;
  popularity_score: number;
  trend_score: number;
  trend_status: 'TRENDING_UP' | 'STABLE' | 'TRENDING_DOWN';
  sentiment_score: number;
  positive_sentiment_pct: number;
  neutral_sentiment_pct: number;
  negative_sentiment_pct: number;
  top_positive_topics?: string[];
  top_negative_topics?: string[];
  created_at: string;
  updated_at: string;
}

export interface RecommendationItem {
  product: Product;
  score: number;
  rank: number;
  reason: string;
  recommendation_type: string;
  signals: {
    content?: number;
    collaborative?: number;
    behavior?: number;
    popularity?: number;
    rating?: number;
    personalization?: number;
    basket_confidence?: number;
  };
}

export interface RecommendationResponse {
  customer_id?: string;
  recommendations: RecommendationItem[];
  count: number;
  model_version: string;
  algorithm: string;
  experiment_group: string;
}

export interface Customer {
  id: string;
  customer_code: string;
  name: string;
  email: string;
  phone?: string;
  age?: number;
  gender?: string;
  location?: string;
  persona: string;
  total_spend: number;
  total_orders: number;
  avg_order_value: number;
  clv_historical: number;
  clv_estimated: number;
  churn_risk_score: number;
  churn_risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  segment_id?: string;
  segment_name?: string;
  favorite_category?: string;
  favorite_brand?: string;
  last_active_at: string;
  created_at: string;
}

export interface CustomerSegment {
  id: string;
  name: string;
  cluster_index: number;
  description?: string;
  customer_count: number;
  avg_spending: number;
  avg_order_value: number;
  avg_purchase_frequency: number;
  avg_churn_risk: number;
  key_characteristics: string[];
}

export interface CustomerInsight {
  customer: Customer;
  recent_interactions: Array<{
    id: string;
    event_type: string;
    product_id: string;
    product_name: string;
    category: string;
    timestamp: string;
  }>;
  top_categories: Array<{ category: string; count: number }>;
  top_brands: Array<{ brand: string; count: number }>;
  journey_funnel: Array<{
    stage: string;
    count: number;
    conversion_rate: number;
    dropoff_rate: number;
  }>;
  recommended_actions: string[];
  clv_breakdown: Record<string, any>;
  churn_factors: string[];
}

export interface LiveActivityItem {
  id: string;
  customer_id: string;
  customer_name?: string;
  product_id?: string;
  product_name?: string;
  event_type: string;
  timestamp: string;
  metadata_json?: Record<string, any>;
}

export interface Review {
  id: string;
  customer_id: string;
  customer_name?: string;
  product_id: string;
  rating: number;
  title?: string;
  comment: string;
  sentiment_label: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
  sentiment_score: number;
  positive_topics: string[];
  negative_topics: string[];
  verified_purchase: number;
  helpful_votes: number;
  created_at: string;
}

export interface CartItem {
  id: string;
  product_id: string;
  product: Product;
  quantity: number;
  unit_price: number;
  total_price: number;
}

export interface Order {
  id: string;
  order_code: string;
  customer_id: string;
  total_amount: number;
  discount_amount: number;
  tax_amount: number;
  final_amount: number;
  status: string;
  payment_method: string;
  created_at: string;
  items: Array<{
    id: string;
    product_id: string;
    product_name: string;
    quantity: number;
    unit_price: number;
    total_price: number;
  }>;
}

export interface OverviewKPIs {
  total_customers: number;
  total_products: number;
  total_orders: number;
  total_revenue: number;
  conversion_rate: number;
  avg_order_value: number;
  active_customers: number;
  recommendation_ctr: number;
  recommendation_revenue_share: number;
}

export interface MLModelVersion {
  id: string;
  model_name: string;
  version: string;
  algorithm: string;
  hyperparameters: Record<string, any>;
  metrics: Record<string, any>;
  is_active: boolean;
  dataset_size: number;
  training_duration_seconds: number;
  trained_by: string;
  created_at: string;
}

export interface ABWeightConfig {
  weight_content: number;
  weight_collaborative: number;
  weight_behavior: number;
  weight_popularity: number;
  weight_rating: number;
  weight_personalization: number;
  active_group: string;
}
