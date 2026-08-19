import React from 'react';
import { Link } from 'react-router-dom';
import { Star, ShoppingCart, Sparkles, TrendingUp, Heart } from 'lucide-react';
import { Product } from '../types';
import { eventsApi } from '../api/client';
import { useAuth } from '../auth/AuthContext';

interface ProductCardProps {
  product: Product;
  recommendationReason?: string;
  recommendationType?: string;
  score?: number;
  onAddToCart?: (product: Product) => void;
  onWishlist?: (product: Product) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  recommendationReason,
  recommendationType,
  score,
  onAddToCart,
  onWishlist
}) => {
  const { user } = useAuth();

  const handleCardClick = () => {
    if (user?.customer_id) {
      eventsApi.track(user.customer_id, 'CLICK_PRODUCT', product.id);
    }
  };

  const discountPrice = product.discount > 0 
    ? (product.price * (1 - product.discount / 100)).toFixed(2)
    : null;

  return (
    <div className="group glass-card glass-card-hover rounded-2xl overflow-hidden flex flex-col justify-between border border-slate-800/80 bg-slate-900/50">
      
      {/* Product Image & Tags Header */}
      <div className="relative aspect-square overflow-hidden bg-slate-950/60 flex items-center justify-center p-4">
        
        {/* Badges Overlay */}
        <div className="absolute top-3 left-3 right-3 flex items-start justify-between z-10 gap-2">
          {recommendationReason ? (
            <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-brand-600/90 text-white text-[10px] font-bold shadow-lg shadow-brand-500/30 backdrop-blur-md">
              <Sparkles className="w-3 h-3 text-brand-200" />
              {recommendationType || 'AI Pick'}
            </span>
          ) : product.trend_status === 'TRENDING_UP' ? (
            <span className="flex items-center gap-1 px-2 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold">
              <TrendingUp className="w-3 h-3" />
              Trending
            </span>
          ) : (
            <span className="px-2 py-0.5 rounded-lg bg-slate-800/80 text-slate-400 border border-slate-700/50 text-[10px] font-medium">
              {product.category}
            </span>
          )}

          {score && (
            <span className="px-2 py-0.5 rounded-md bg-slate-900/90 text-brand-300 border border-brand-500/30 text-[10px] font-bold">
              {(score * 100).toFixed(0)}% Match
            </span>
          )}
        </div>

        {/* Product Image */}
        <Link 
          to={`/products/${product.id}`}
          onClick={handleCardClick}
          className="w-full h-full flex items-center justify-center"
        >
          <img
            src={product.image_url || "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"}
            alt={product.name}
            className="object-contain max-h-44 group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
        </Link>
      </div>

      {/* Product Content Body */}
      <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
        
        <div>
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
            <span className="font-semibold text-brand-400">{product.brand}</span>
            <div className="flex items-center gap-1 text-amber-400 font-medium">
              <Star className="w-3.5 h-3.5 fill-amber-400" />
              <span>{product.rating.toFixed(1)}</span>
              <span className="text-slate-500 text-[10px]">({product.rating_count})</span>
            </div>
          </div>

          <Link 
            to={`/products/${product.id}`}
            onClick={handleCardClick}
            className="block font-bold text-sm text-slate-100 hover:text-brand-300 transition-colors line-clamp-1"
          >
            {product.name}
          </Link>

          {/* AI Recommendation Explainability Reason */}
          {recommendationReason ? (
            <p className="mt-1 text-[11px] text-slate-400 line-clamp-2 italic bg-brand-950/20 p-1.5 rounded-lg border border-brand-500/10">
              "{recommendationReason}"
            </p>
          ) : (
            <p className="mt-1 text-[11px] text-slate-400 line-clamp-2">
              {product.description}
            </p>
          )}
        </div>

        {/* Price & Add to Cart Footer */}
        <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between gap-2">
          <div>
            <div className="flex items-baseline gap-1.5">
              <span className="text-base font-extrabold text-white">
                ${discountPrice || product.price.toFixed(2)}
              </span>
              {discountPrice && (
                <span className="text-xs text-slate-500 line-through">
                  ${product.price.toFixed(2)}
                </span>
              )}
            </div>
            <div className="text-[10px] text-emerald-400 font-medium">
              {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
            </div>
          </div>

          <div className="flex items-center gap-1.5">
            {onWishlist && (
              <button
                onClick={() => onWishlist(product)}
                className="p-2 rounded-xl bg-slate-800/60 hover:bg-rose-500/20 hover:text-rose-400 text-slate-400 border border-slate-700/50 transition-colors"
                title="Add to Wishlist"
              >
                <Heart className="w-4 h-4" />
              </button>
            )}
            {onAddToCart && (
              <button
                onClick={() => onAddToCart(product)}
                className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold shadow-md shadow-brand-600/20 transition-all active:scale-95"
              >
                <ShoppingCart className="w-3.5 h-3.5" />
                <span>Add</span>
              </button>
            )}
          </div>

        </div>

      </div>

    </div>
  );
};
