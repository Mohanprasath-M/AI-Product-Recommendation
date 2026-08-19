import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Star, 
  ShoppingCart, 
  Heart, 
  Sparkles, 
  TrendingUp, 
  ShieldCheck, 
  ThumbsUp, 
  ThumbsDown,
  MessageSquare,
  Send,
  Boxes,
  CheckCircle2
} from 'lucide-react';
import { productsApi, recommendationsApi, reviewsApi, eventsApi, ordersApi } from '../api/client';
import { Product, RecommendationItem, Review } from '../types';
import { ProductCard } from '../components/ProductCard';
import { useAuth } from '../auth/AuthContext';

interface ProductDetailProps {
  onAddToCart: (product: Product) => void;
}

export const ProductDetail: React.FC<ProductDetailProps> = ({ onAddToCart }) => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  
  const [product, setProduct] = useState<Product | null>(null);
  const [similarProducts, setSimilarProducts] = useState<RecommendationItem[]>([]);
  const [boughtTogether, setBoughtTogether] = useState<RecommendationItem[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [sentimentSummary, setSentimentSummary] = useState<any>(null);

  const [reviewRating, setReviewRating] = useState(5);
  const [reviewComment, setReviewComment] = useState('');
  const [isSubmittingReview, setIsSubmittingReview] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState(false);

  const loadData = async () => {
    if (!id) return;
    try {
      // Track VIEW_PRODUCT event
      if (user?.customer_id) {
        eventsApi.track(user.customer_id, 'VIEW_PRODUCT', id);
      }

      const [p, sim, tog, revs, summ] = await Promise.all([
        productsApi.get(id),
        recommendationsApi.getSimilar(id, 4),
        recommendationsApi.getBoughtTogether(id, 4),
        reviewsApi.getProductReviews(id, 10),
        reviewsApi.getSummary(id)
      ]);

      setProduct(p);
      setSimilarProducts(sim || []);
      setBoughtTogether(tog || []);
      setReviews(revs || []);
      setSentimentSummary(summ);
    } catch (e) {
      console.error('Failed to load product details:', e);
    }
  };

  useEffect(() => {
    loadData();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [id]);

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !reviewComment.trim()) return;
    setIsSubmittingReview(true);
    try {
      await reviewsApi.createReview({
        product_id: id,
        customer_id: user?.customer_id,
        rating: reviewRating,
        title: `${reviewRating} Star Feedback`,
        comment: reviewComment
      });
      setReviewComment('');
      setReviewSuccess(true);
      setTimeout(() => setReviewSuccess(false), 4000);
      loadData();
    } catch (err) {
      console.error('Error posting review:', err);
    } finally {
      setIsSubmittingReview(false);
    }
  };

  if (!product) {
    return (
      <div className="py-20 text-center">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-sm text-slate-400">Loading intelligence profile...</p>
      </div>
    );
  }

  return (
    <div className="space-y-12 pb-16">
      
      {/* Product Hero Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        
        {/* Left: Product Showcase Image */}
        <div className="glass-card rounded-3xl p-8 border border-slate-800 bg-slate-900/50 flex items-center justify-center relative">
          {product.trend_status === 'TRENDING_UP' && (
            <span className="absolute top-6 left-6 flex items-center gap-1.5 px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold">
              <TrendingUp className="w-4 h-4" />
              Surging Customer Demand
            </span>
          )}
          <img
            src={product.image_url || "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"}
            alt={product.name}
            className="max-h-96 object-contain drop-shadow-2xl"
          />
        </div>

        {/* Right: Product Metadata & Actions */}
        <div className="space-y-6 flex flex-col justify-between">
          
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-xs">
              <span className="font-bold text-brand-400 uppercase tracking-wider">{product.brand}</span>
              <span className="text-slate-600">•</span>
              <span className="text-slate-400">{product.category}</span>
              <span className="text-slate-600">•</span>
              <span className="font-mono text-slate-500">{product.product_code}</span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-white">{product.name}</h1>

            {/* Rating Bar */}
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1 text-amber-400 font-bold text-sm">
                <Star className="w-4 h-4 fill-amber-400" />
                <span>{product.rating.toFixed(1)}</span>
              </div>
              <span className="text-xs text-slate-400 font-medium">({product.rating_count} reviews)</span>
              <span className="text-slate-700">•</span>
              <span className="text-xs text-emerald-400 font-bold">{product.views_count} Views Tracked</span>
            </div>

            {/* Price block */}
            <div className="flex items-baseline gap-3 pt-2">
              <span className="text-3xl font-black text-white">${product.price.toFixed(2)}</span>
              {product.discount > 0 && (
                <span className="px-2 py-0.5 rounded-lg bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-bold">
                  {product.discount}% OFF
                </span>
              )}
            </div>

            <p className="text-sm text-slate-300 leading-relaxed">{product.description}</p>
          </div>

          {/* Action Buttons */}
          <div className="space-y-4 pt-6 border-t border-slate-800">
            <div className="flex items-center gap-3">
              <button
                onClick={() => onAddToCart(product)}
                className="flex-1 flex items-center justify-center gap-2 py-3.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-sm font-bold shadow-lg shadow-brand-600/30 transition-all active:scale-95"
              >
                <ShoppingCart className="w-4 h-4" />
                <span>Add to Cart</span>
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs text-slate-400">
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Stock: {product.stock} units</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-brand-400" />
                <span>AI Popularity: {(product.popularity_score * 100).toFixed(0)}/100</span>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* NLP Sentiment & Topic Intelligence Breakdown */}
      <div className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/40 space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-black text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-brand-400" />
              NLP Review Sentiment & Topic Extraction
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Locally processed using TF-IDF + Logistic Regression classification on customer comments.
            </p>
          </div>
        </div>

        {sentimentSummary && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Sentiment Meter */}
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Sentiment Ratio</div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-emerald-400 font-semibold">Positive</span>
                  <span className="text-slate-200 font-bold">{sentimentSummary.positive_pct}%</span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden flex">
                  <div className="bg-emerald-500 h-full" style={{ width: `${sentimentSummary.positive_pct}%` }} />
                  <div className="bg-slate-500 h-full" style={{ width: `${sentimentSummary.neutral_pct}%` }} />
                  <div className="bg-rose-500 h-full" style={{ width: `${sentimentSummary.negative_pct}%` }} />
                </div>
                <div className="flex justify-between text-[11px] text-slate-500">
                  <span>Neutral: {sentimentSummary.neutral_pct}%</span>
                  <span>Negative: {sentimentSummary.negative_pct}%</span>
                </div>
              </div>
            </div>

            {/* Positive Keyword Topics */}
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
              <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-400 uppercase tracking-wider">
                <ThumbsUp className="w-3.5 h-3.5" />
                <span>Frequently Praised Topics</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {sentimentSummary.top_positive_topics?.length > 0 ? (
                  sentimentSummary.top_positive_topics.map((t: any, i: number) => (
                    <span key={i} className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 text-xs font-semibold">
                      +{t.topic}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500">Sound quality, comfort, durability</span>
                )}
              </div>
            </div>

            {/* Negative Keyword Topics */}
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-3">
              <div className="flex items-center gap-1.5 text-xs font-bold text-rose-400 uppercase tracking-wider">
                <ThumbsDown className="w-3.5 h-3.5" />
                <span>Customer Pain Points</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {sentimentSummary.top_negative_topics?.length > 0 ? (
                  sentimentSummary.top_negative_topics.map((t: any, i: number) => (
                    <span key={i} className="px-2.5 py-1 rounded-lg bg-rose-500/10 text-rose-300 border border-rose-500/20 text-xs font-semibold">
                      -{t.topic}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500">No major negative trends detected</span>
                )}
              </div>
            </div>

          </div>
        )}
      </div>

      {/* Frequently Bought Together Section */}
      {boughtTogether.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Boxes className="w-5 h-5 text-indigo-400" />
            <h2 className="text-xl font-extrabold text-white">Frequently Bought Together</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {boughtTogether.map((item) => (
              <ProductCard
                key={item.product.id}
                product={item.product}
                recommendationReason={item.reason}
                recommendationType="BASKET"
                onAddToCart={onAddToCart}
              />
            ))}
          </div>
        </div>
      )}

      {/* Similar Products Recommendation */}
      {similarProducts.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-brand-400" />
            <h2 className="text-xl font-extrabold text-white">Similar Products (Content-Based)</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {similarProducts.map((item) => (
              <ProductCard
                key={item.product.id}
                product={item.product}
                recommendationReason={item.reason}
                recommendationType="CONTENT"
                score={item.score}
                onAddToCart={onAddToCart}
              />
            ))}
          </div>
        </div>
      )}

      {/* Customer Reviews & Post Review Form */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pt-4">
        
        {/* Review Submission Form */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4 h-fit">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-4 h-4 text-brand-400" />
            <h3 className="text-base font-bold text-white">Write a Review</h3>
          </div>
          
          <form onSubmit={handleSubmitReview} className="space-y-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Your Rating</label>
              <div className="flex items-center gap-1.5">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setReviewRating(star)}
                    className="p-1"
                  >
                    <Star className={`w-5 h-5 ${star <= reviewRating ? 'fill-amber-400 text-amber-400' : 'text-slate-600'}`} />
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Review Comment</label>
              <textarea
                value={reviewComment}
                onChange={(e) => setReviewComment(e.target.value)}
                placeholder="Share your experience (NLP analyzer will classify positive/negative feedback)..."
                rows={4}
                className="w-full bg-slate-950 border border-slate-800 focus:border-brand-500 rounded-xl p-3 text-xs text-slate-100 placeholder-slate-500 focus:outline-none"
                required
              />
            </div>

            {reviewSuccess && (
              <div className="flex items-center gap-2 p-2.5 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold">
                <CheckCircle2 className="w-4 h-4" />
                <span>Review posted & analyzed with NLP!</span>
              </div>
            )}

            <button
              type="submit"
              disabled={isSubmittingReview}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold transition-all disabled:opacity-50"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{isSubmittingReview ? 'Analyzing & Posting...' : 'Submit Review'}</span>
            </button>
          </form>
        </div>

        {/* Reviews List */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-base font-bold text-white">Customer Reviews ({reviews.length})</h3>
          
          <div className="space-y-3">
            {reviews.length === 0 ? (
              <div className="text-center py-8 glass-card rounded-2xl text-xs text-slate-500">
                Be the first to review this product!
              </div>
            ) : (
              reviews.map((rev) => (
                <div key={rev.id} className="glass-card rounded-2xl p-4 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-slate-800 flex items-center justify-center text-[10px] font-bold text-slate-300">
                        {rev.customer_name?.charAt(0) || 'U'}
                      </div>
                      <span className="text-xs font-bold text-slate-200">{rev.customer_name}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold ${
                        rev.sentiment_label === 'POSITIVE'
                          ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                          : rev.sentiment_label === 'NEGATIVE'
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                          : 'bg-slate-800 text-slate-400'
                      }`}>
                        NLP: {rev.sentiment_label}
                      </span>
                      <div className="flex text-amber-400">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={`w-3 h-3 ${i < rev.rating ? 'fill-amber-400' : 'text-slate-700'}`} />
                        ))}
                      </div>
                    </div>
                  </div>

                  <p className="text-xs text-slate-300">{rev.comment}</p>
                </div>
              ))
            )}
          </div>
        </div>

      </div>

    </div>
  );
};
