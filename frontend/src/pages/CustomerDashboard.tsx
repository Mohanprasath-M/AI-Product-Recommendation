import React, { useState, useEffect } from 'react';
import { Sparkles, TrendingUp, Zap, ShoppingBag, ArrowRight, ShieldCheck, RefreshCw } from 'lucide-react';
import { ProductCard } from '../components/ProductCard';
import { recommendationsApi, productsApi, ordersApi } from '../api/client';
import { RecommendationItem, Product, CartItem } from '../types';
import { useAuth } from '../auth/AuthContext';

interface CustomerDashboardProps {
  onAddToCart: (product: Product) => void;
}

export const CustomerDashboard: React.FC<CustomerDashboardProps> = ({ onAddToCart }) => {
  const { user } = useAuth();
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [trendingProducts, setTrendingProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  const fetchFeeds = async () => {
    setIsLoading(true);
    try {
      const custId = user?.customer_id || 'c1';
      const [recData, trendData, catData] = await Promise.all([
        recommendationsApi.getPersonalized(custId, 8, selectedCategory),
        productsApi.list({ sort_by: 'trending', size: 4 }),
        productsApi.getCategories()
      ]);
      setRecommendations(recData.recommendations || []);
      setTrendingProducts(trendData.items || []);
      setCategories(catData || []);
    } catch (e) {
      console.error('Failed to fetch recommendation feed:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFeeds();
  }, [user?.customer_id, selectedCategory]);

  return (
    <div className="space-y-8 pb-12">
      
      {/* Hero Welcome Banner */}
      <div className="relative rounded-3xl overflow-hidden glass-card border border-brand-500/20 bg-gradient-to-r from-brand-950/60 via-slate-900/80 to-indigo-950/60 p-8 sm:p-10 shadow-2xl">
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-brand-500/10 blur-3xl pointer-events-none" />
        
        <div className="max-w-2xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30 text-xs font-bold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Real-Time Hybrid Recommendation Engine Active</span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
            Welcome back, <span className="bg-gradient-to-r from-brand-300 via-indigo-200 to-white bg-clip-text text-transparent">{user?.full_name || 'Alex'}</span>
          </h1>

          <p className="text-sm text-slate-300 leading-relaxed">
            Your personalized feed is curated in real-time using content similarity, matrix factorization SVD, and live browsing intent.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3 text-xs text-slate-400">
            <div className="flex items-center gap-1.5 bg-slate-900/80 px-3 py-1.5 rounded-xl border border-slate-800">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>100% On-Device ML (No External API Latency)</span>
            </div>
            <button
              onClick={fetchFeeds}
              className="flex items-center gap-1.5 bg-brand-600/20 hover:bg-brand-600/30 text-brand-300 px-3 py-1.5 rounded-xl border border-brand-500/30 transition-colors font-semibold"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Recalculate Signals</span>
            </button>
          </div>
        </div>
      </div>

      {/* Category Pills Filter */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">Filter by Interest Domain</h2>
          {selectedCategory && (
            <button
              onClick={() => setSelectedCategory(undefined)}
              className="text-xs font-semibold text-brand-400 hover:text-brand-300"
            >
              Clear Filter
            </button>
          )}
        </div>

        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          <button
            onClick={() => setSelectedCategory(undefined)}
            className={`px-4 py-2 rounded-xl text-xs font-bold shrink-0 transition-all ${
              selectedCategory === undefined
                ? 'bg-brand-600 text-white shadow-lg shadow-brand-600/20'
                : 'bg-slate-900 text-slate-300 border border-slate-800 hover:bg-slate-800'
            }`}
          >
            All Products
          </button>
          {categories.map((c) => (
            <button
              key={c.id}
              onClick={() => setSelectedCategory(c.name)}
              className={`px-4 py-2 rounded-xl text-xs font-bold shrink-0 transition-all ${
                selectedCategory === c.name
                  ? 'bg-brand-600 text-white shadow-lg shadow-brand-600/20'
                  : 'bg-slate-900 text-slate-300 border border-slate-800 hover:bg-slate-800'
              }`}
            >
              {c.name}
            </button>
          ))}
        </div>
      </div>

      {/* Primary Section: Personalized AI Recommendations */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-brand-400" />
              <h2 className="text-xl font-extrabold text-white">Recommended For You</h2>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Ranked with transparent explainability tags based on your shopping affinity.
            </p>
          </div>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
              <div key={n} className="rounded-2xl glass-card h-80 animate-pulse bg-slate-900/40" />
            ))}
          </div>
        ) : recommendations.length === 0 ? (
          <div className="text-center py-12 glass-card rounded-2xl">
            <p className="text-sm text-slate-400">No recommendations found for this category.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {recommendations.map((rec) => (
              <ProductCard
                key={rec.product.id}
                product={rec.product}
                recommendationReason={rec.reason}
                recommendationType={rec.recommendation_type}
                score={rec.score}
                onAddToCart={onAddToCart}
              />
            ))}
          </div>
        )}
      </div>

      {/* Trending Velocity Section */}
      <div className="space-y-4 pt-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            <h2 className="text-xl font-extrabold text-white">Trending in Real Time</h2>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {trendingProducts.map((p) => (
            <ProductCard
              key={p.id}
              product={p}
              onAddToCart={onAddToCart}
            />
          ))}
        </div>
      </div>

    </div>
  );
};
