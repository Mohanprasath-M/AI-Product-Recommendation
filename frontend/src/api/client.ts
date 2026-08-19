import axios from 'axios';
import {
  AuthResponse,
  Product,
  Customer,
  CustomerSegment,
  CustomerInsight,
  RecommendationResponse,
  RecommendationItem,
  Review,
  CartItem,
  Order,
  OverviewKPIs,
  MLModelVersion,
  ABWeightConfig,
  LiveActivityItem
} from '../types';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('nexus_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Optional: auto-redirect to login if not already on login page
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (email: string, password: string): Promise<AuthResponse> => {
    const res = await api.post('/auth/login', { email, password });
    return res.data;
  },
  register: async (data: { email: string; password: string; full_name: string; role?: string }): Promise<AuthResponse> => {
    const res = await api.post('/auth/register', data);
    return res.data;
  },
  getMe: async () => {
    const res = await api.get('/auth/me');
    return res.data;
  }
};

export const productsApi = {
  list: async (params?: any) => {
    const res = await api.get('/products', { params });
    return res.data;
  },
  get: async (id: string): Promise<Product> => {
    const res = await api.get(`/products/${id}`);
    return res.data;
  },
  create: async (data: Partial<Product>): Promise<Product> => {
    const res = await api.post('/products', data);
    return res.data;
  },
  update: async (id: string, data: Partial<Product>): Promise<Product> => {
    const res = await api.put(`/products/${id}`, data);
    return res.data;
  },
  updateStock: async (id: string, stock: number): Promise<Product> => {
    const res = await api.patch(`/products/${id}/stock`, { stock });
    return res.data;
  },
  delete: async (id: string) => {
    const res = await api.delete(`/products/${id}`);
    return res.data;
  },
  getCategories: async () => {
    const res = await api.get('/products/categories');
    return res.data;
  },
  getBrands: async () => {
    const res = await api.get('/products/brands');
    return res.data;
  }
};

export const recommendationsApi = {
  getPersonalized: async (customerId: string, limit = 10, category?: string): Promise<RecommendationResponse> => {
    const res = await api.get(`/recommendations/${customerId}`, { params: { limit, category } });
    return res.data;
  },
  getSimilar: async (productId: string, limit = 6): Promise<RecommendationItem[]> => {
    const res = await api.get(`/recommendations/product/${productId}/similar`, { params: { limit } });
    return res.data;
  },
  getBoughtTogether: async (productId: string, limit = 4): Promise<RecommendationItem[]> => {
    const res = await api.get(`/recommendations/product/${productId}/bought-together`, { params: { limit } });
    return res.data;
  },
  trackFeedback: async (feedback: { productId: string; customerId: string; action: string; rank: number; recommendationType: string }) => {
    const res = await api.post('/recommendations/feedback', {
      product_id: feedback.productId,
      customer_id: feedback.customerId,
      action: feedback.action,
      rank: feedback.rank,
      recommendation_type: feedback.recommendationType
    });
    return res.data;
  },
  getWeights: async (): Promise<ABWeightConfig> => {
    const res = await api.get('/recommendations/config/weights');
    return res.data;
  },
  updateWeights: async (weights: ABWeightConfig): Promise<ABWeightConfig> => {
    const res = await api.post('/recommendations/config/weights', weights);
    return res.data;
  }
};

export const customersApi = {
  list: async (params?: any) => {
    const res = await api.get('/customers', { params });
    return res.data;
  },
  get: async (id: string): Promise<Customer> => {
    const res = await api.get(`/customers/${id}`);
    return res.data;
  },
  getInsights: async (id: string): Promise<CustomerInsight> => {
    const res = await api.get(`/customers/${id}/insights`);
    return res.data;
  },
  getSegments: async (): Promise<CustomerSegment[]> => {
    const res = await api.get('/customers/segments');
    return res.data;
  }
};

export const eventsApi = {
  track: async (customerId: string, eventType: string, productId?: string, metadata?: any) => {
    const res = await api.post('/events/track', {
      customer_id: customerId,
      event_type: eventType,
      product_id: productId,
      metadata_json: metadata || {}
    });
    return res.data;
  },
  trackSearch: async (query: string, customerId?: string, resultCount = 0, clickedProductId?: string) => {
    const res = await api.post('/events/search', {
      query,
      customer_id: customerId,
      result_count: resultCount,
      clicked_product_id: clickedProductId
    });
    return res.data;
  },
  getLiveEvents: async (limit = 20): Promise<LiveActivityItem[]> => {
    const res = await api.get('/events/live', { params: { limit } });
    return res.data;
  }
};

export const ordersApi = {
  getCart: async (customerId: string): Promise<CartItem[]> => {
    const res = await api.get(`/orders/cart/${customerId}`);
    return res.data;
  },
  addToCart: async (customerId: string, productId: string, quantity = 1): Promise<CartItem> => {
    const res = await api.post(`/orders/cart/${customerId}`, { product_id: productId, quantity });
    return res.data;
  },
  removeFromCart: async (customerId: string, productId: string) => {
    const res = await api.delete(`/orders/cart/${customerId}/${productId}`);
    return res.data;
  },
  checkout: async (customerId: string, items: Array<{ product_id: string; quantity: number }>): Promise<Order> => {
    const res = await api.post(`/orders/checkout/${customerId}`, { items });
    return res.data;
  },
  getHistory: async (customerId: string): Promise<Order[]> => {
    const res = await api.get(`/orders/history/${customerId}`);
    return res.data;
  }
};

export const reviewsApi = {
  getProductReviews: async (productId: string, limit = 20): Promise<Review[]> => {
    const res = await api.get(`/reviews/product/${productId}`, { params: { limit } });
    return res.data;
  },
  getSummary: async (productId: string) => {
    const res = await api.get(`/reviews/product/${productId}/summary`);
    return res.data;
  },
  createReview: async (data: { product_id: string; customer_id?: string; rating: number; title?: string; comment: string }): Promise<Review> => {
    const res = await api.post('/reviews', data);
    return res.data;
  }
};

export const analyticsApi = {
  getOverview: async (): Promise<OverviewKPIs> => {
    const res = await api.get('/analytics/overview');
    return res.data;
  },
  getRevenueTrends: async (days = 14) => {
    const res = await api.get('/analytics/revenue-trends', { params: { days } });
    return res.data;
  },
  getCategoryPerformance: async () => {
    const res = await api.get('/analytics/category-performance');
    return res.data;
  },
  getConversionFunnel: async () => {
    const res = await api.get('/analytics/conversion-funnel');
    return res.data;
  },
  getTopProducts: async (limit = 6) => {
    const res = await api.get('/analytics/top-products', { params: { limit } });
    return res.data;
  },
  getAtRiskCustomers: async (limit = 6) => {
    const res = await api.get('/analytics/at-risk-customers', { params: { limit } });
    return res.data;
  },
  getSearchAnalytics: async () => {
    const res = await api.get('/analytics/search-analytics');
    return res.data;
  }
};

export const mlApi = {
  getModels: async (): Promise<MLModelVersion[]> => {
    const res = await api.get('/ml/models');
    return res.data;
  },
  getEvaluations: async () => {
    const res = await api.get('/ml/evaluation');
    return res.data;
  },
  triggerTraining: async (modelType = 'ALL') => {
    const res = await api.post('/ml/train', { model_type: modelType, force_retrain: true });
    return res.data;
  }
};

export const healthApi = {
  checkAll: async () => {
    const [main, db, redis, ml] = await Promise.all([
      api.get('/health'),
      api.get('/health/database'),
      api.get('/health/redis'),
      api.get('/health/ml')
    ]);
    return {
      main: main.data,
      database: db.data,
      redis: redis.data,
      ml: ml.data
    };
  }
};
