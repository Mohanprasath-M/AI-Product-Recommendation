import React from 'react';
import { Radio, Eye, MousePointerClick, ShoppingCart, CreditCard, Heart, Star } from 'lucide-react';
import { LiveActivityItem } from '../types';

interface LiveStreamFeedProps {
  events: LiveActivityItem[];
  maxItems?: number;
}

export const LiveStreamFeed: React.FC<LiveStreamFeedProps> = ({ events, maxItems = 8 }) => {
  const getEventBadge = (type: string) => {
    switch (type) {
      case 'PURCHASE':
        return { icon: CreditCard, color: 'text-emerald-400 bg-emerald-500/20 border-emerald-500/30', label: 'Purchase' };
      case 'ADD_TO_CART':
        return { icon: ShoppingCart, color: 'text-brand-400 bg-brand-500/20 border-brand-500/30', label: 'Cart Add' };
      case 'ADD_TO_WISHLIST':
        return { icon: Heart, color: 'text-rose-400 bg-rose-500/20 border-rose-500/30', label: 'Wishlist' };
      case 'REVIEW':
        return { icon: Star, color: 'text-amber-400 bg-amber-500/20 border-amber-500/30', label: 'Review' };
      case 'CLICK_PRODUCT':
        return { icon: MousePointerClick, color: 'text-cyan-400 bg-cyan-500/20 border-cyan-500/30', label: 'Click' };
      default:
        return { icon: Eye, color: 'text-slate-400 bg-slate-800 border-slate-700', label: 'View' };
    }
  };

  return (
    <div className="glass-card rounded-2xl p-5 border border-slate-800/80 bg-slate-900/60">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-200">Real-Time Event Stream</h3>
        </div>
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
          Live WebSocket
        </span>
      </div>

      <div className="mt-3 space-y-2.5 max-h-80 overflow-y-auto pr-1">
        {events.length === 0 ? (
          <div className="text-center py-6 text-xs text-slate-500">
            Waiting for live incoming customer events...
          </div>
        ) : (
          events.slice(0, maxItems).map((ev) => {
            const badge = getEventBadge(ev.event_type);
            const Icon = badge.icon;
            return (
              <div
                key={ev.id || Math.random()}
                className="flex items-center justify-between p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/60 text-xs animate-in fade-in slide-in-from-top-1"
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center border shrink-0 ${badge.color}`}>
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  <div className="truncate">
                    <div className="font-semibold text-slate-200 truncate">
                      {ev.customer_name || 'Customer'}{' '}
                      <span className="font-normal text-slate-400">
                        {ev.event_type.replace('_', ' ').toLowerCase()}
                      </span>
                    </div>
                    {ev.product_name && (
                      <div className="text-[11px] text-brand-400 truncate">{ev.product_name}</div>
                    )}
                  </div>
                </div>

                <span className="text-[10px] text-slate-500 shrink-0 ml-2">
                  {new Date(ev.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
