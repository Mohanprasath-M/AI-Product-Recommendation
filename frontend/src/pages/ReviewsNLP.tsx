import React, { useState, useEffect } from 'react';
import { MessageSquareText, ThumbsUp, ThumbsDown, Sparkles, RefreshCw } from 'lucide-react';
import { reviewsApi, productsApi } from '../api/client';
import { Product } from '../types';

export const ReviewsNLP: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [summary, setSummary] = useState<any>(null);
  const [reviews, setReviews] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const pData = await productsApi.list({ size: 10, sort_by: 'rating' });
      setProducts(pData.items || []);
      if (pData.items && pData.items.length > 0) {
        const first = pData.items[0];
        setSelectedProduct(first);
        const [sumData, revData] = await Promise.all([
          reviewsApi.getSummary(first.id),
          reviewsApi.getProductReviews(first.id, 10)
        ]);
        setSummary(sumData);
        setReviews(revData || []);
      }
    } catch (e) {
      console.error('Failed to load review NLP intelligence:', e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectProduct = async (p: Product) => {
    setSelectedProduct(p);
    try {
      const [sumData, revData] = await Promise.all([
        reviewsApi.getSummary(p.id),
        reviewsApi.getProductReviews(p.id, 10)
      ]);
      setSummary(sumData);
      setReviews(revData || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-8 pb-16">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30 text-xs font-bold uppercase tracking-wider">
              Local NLP Suite
            </span>
            <span className="text-xs text-slate-400 font-medium">TF-IDF Vectorizer + Logistic Classifier</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white mt-1">Review Sentiment & Topic Extraction</h1>
        </div>

        <button
          onClick={loadData}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-bold text-slate-200"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh NLP Feed</span>
        </button>
      </div>

      {/* Select Product Filter */}
      <div className="glass-card rounded-2xl p-4 border border-slate-800 flex items-center gap-3 overflow-x-auto">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400 shrink-0">Select Product:</span>
        <div className="flex gap-2">
          {products.map((p) => (
            <button
              key={p.id}
              onClick={() => handleSelectProduct(p)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold shrink-0 transition-all ${
                selectedProduct?.id === p.id
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-600/30'
                  : 'bg-slate-950 text-slate-300 border border-slate-800 hover:bg-slate-900'
              }`}
            >
              {p.name.slice(0, 25)}...
            </button>
          ))}
        </div>
      </div>

      {/* Selected Product NLP Intelligence */}
      {selectedProduct && summary && (
        <div className="space-y-6">
          <div className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/50 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
              <div>
                <h2 className="text-xl font-extrabold text-white">{selectedProduct.name}</h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  {selectedProduct.brand} • {selectedProduct.category} • Average Rating: {summary.average_rating}★ ({summary.total_reviews} reviews)
                </p>
              </div>
            </div>

            {/* Sentiment Meter & Topic Cloud */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Sentiment Distribution</div>
                <div className="space-y-2">
                  <div className="flex justify-between text-xs">
                    <span className="text-emerald-400 font-semibold">Positive Feedback</span>
                    <span className="text-white font-bold">{summary.positive_pct}%</span>
                  </div>
                  <div className="w-full h-2.5 rounded-full bg-slate-800 overflow-hidden flex">
                    <div className="bg-emerald-500 h-full" style={{ width: `${summary.positive_pct}%` }} />
                    <div className="bg-slate-500 h-full" style={{ width: `${summary.neutral_pct}%` }} />
                    <div className="bg-rose-500 h-full" style={{ width: `${summary.negative_pct}%` }} />
                  </div>
                  <div className="flex justify-between text-[11px] text-slate-400 pt-1">
                    <span>Neutral: {summary.neutral_pct}%</span>
                    <span>Negative: {summary.negative_pct}%</span>
                  </div>
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-400 uppercase tracking-wider">
                  <ThumbsUp className="w-3.5 h-3.5" />
                  <span>Top Positive Topics</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {summary.top_positive_topics?.map((t: any, i: number) => (
                    <span key={i} className="px-3 py-1.5 rounded-xl bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 text-xs font-bold">
                      +{t.topic}
                    </span>
                  ))}
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                <div className="flex items-center gap-1.5 text-xs font-bold text-rose-400 uppercase tracking-wider">
                  <ThumbsDown className="w-3.5 h-3.5" />
                  <span>Top Negative Topics</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {summary.top_negative_topics?.map((t: any, i: number) => (
                    <span key={i} className="px-3 py-1.5 rounded-xl bg-rose-500/10 text-rose-300 border border-rose-500/20 text-xs font-bold">
                      -{t.topic}
                    </span>
                  ))}
                </div>
              </div>

            </div>
          </div>

          {/* Detailed Review Sentiment Inspection List */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-white">Classified Review Comments Feed</h3>
            <div className="space-y-3">
              {reviews.map((r) => (
                <div key={r.id} className="glass-card rounded-2xl p-4 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-slate-200">{r.customer_name}</span>
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                      r.sentiment_label === 'POSITIVE'
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                        : r.sentiment_label === 'NEGATIVE'
                        ? 'bg-rose-500/20 text-rose-300 border-rose-500/30'
                        : 'bg-slate-800 text-slate-400 border-slate-700'
                    }`}>
                      NLP: {r.sentiment_label} (Score: {r.sentiment_score})
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">{r.comment}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
