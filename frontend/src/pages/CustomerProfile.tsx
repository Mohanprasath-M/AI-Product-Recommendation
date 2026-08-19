import React, { useState, useEffect } from 'react';
import { 
  User, 
  DollarSign, 
  ShoppingBag, 
  Activity, 
  ShieldAlert, 
  Sparkles, 
  Clock, 
  ArrowRight,
  TrendingUp,
  Tag
} from 'lucide-react';
import { customersApi } from '../api/client';
import { CustomerInsight } from '../types';
import { useAuth } from '../auth/AuthContext';

export const CustomerProfile: React.FC = () => {
  const { user } = useAuth();
  const [insight, setInsight] = useState<CustomerInsight | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchInsight = async () => {
      if (!user?.customer_id) return;
      setIsLoading(true);
      try {
        const data = await customersApi.getInsights(user.customer_id);
        setInsight(data);
      } catch (e) {
        console.error('Failed to load customer insight:', e);
      } finally {
        setIsLoading(false);
      }
    };
    fetchInsight();
  }, [user?.customer_id]);

  if (isLoading || !insight) {
    return (
      <div className="py-20 text-center">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-sm text-slate-400">Loading intelligence profile...</p>
      </div>
    );
  }

  const cust = insight.customer;

  return (
    <div className="space-y-8 pb-16">
      
      {/* Profile Header Card */}
      <div className="glass-card rounded-3xl p-8 border border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900/80 to-brand-950/40 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-xl font-extrabold text-white shadow-xl shadow-brand-500/20">
              {cust.name.charAt(0)}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-black text-white">{cust.name}</h1>
                <span className="px-2.5 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30 text-xs font-bold">
                  {cust.segment_name || cust.persona}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">{cust.email} • {cust.customer_code} • {cust.location}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className={`px-3 py-1.5 rounded-xl border text-xs font-bold flex items-center gap-1.5 ${
              cust.churn_risk_level === 'HIGH'
                ? 'bg-rose-500/20 text-rose-300 border-rose-500/30'
                : cust.churn_risk_level === 'MEDIUM'
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/30'
                : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
            }`}>
              <ShieldAlert className="w-4 h-4" />
              <span>Churn Risk: {cust.churn_risk_level} ({(cust.churn_risk_score * 100).toFixed(0)}%)</span>
            </span>
          </div>
        </div>

        {/* Top KPI row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-slate-800">
          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Total Spend</div>
            <div className="text-xl font-black text-white mt-1">${cust.total_spend.toFixed(2)}</div>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Total Orders</div>
            <div className="text-xl font-black text-white mt-1">{cust.total_orders}</div>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Average Order Value</div>
            <div className="text-xl font-black text-white mt-1">${cust.avg_order_value.toFixed(2)}</div>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800">
            <div className="text-[11px] font-bold uppercase tracking-wider text-brand-400">Estimated CLV</div>
            <div className="text-xl font-black text-brand-300 mt-1">${cust.clv_estimated.toFixed(2)}</div>
          </div>
        </div>
      </div>

      {/* Customer Journey Conversion Funnel */}
      <div className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/50 space-y-6">
        <div>
          <h2 className="text-lg font-black text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-brand-400" />
            Customer Behavioral Journey Funnel
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Tracking individual conversion stages from initial query through completed purchase.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {insight.journey_funnel.map((step, idx) => (
            <div key={idx} className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-2 text-center relative">
              <div className="text-xs font-bold text-slate-400 uppercase">{step.stage}</div>
              <div className="text-xl font-black text-white">{step.count}</div>
              <div className="text-[11px] text-emerald-400 font-semibold">{step.conversion_rate}% rate</div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommended Next Actions & Recent Timeline */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Next Best Actions */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-bold text-white">Recommended AI Retention Actions</h3>
          </div>
          <div className="space-y-2.5">
            {insight.recommended_actions.map((act, i) => (
              <div key={i} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs text-slate-200 flex items-start gap-2.5">
                <ArrowRight className="w-4 h-4 text-brand-400 shrink-0 mt-0.5" />
                <span>{act}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity Timeline */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base font-bold text-white">Recent Real-Time Activity</h3>
          </div>
          <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
            {insight.recent_interactions.map((it) => (
              <div key={it.id} className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/60 flex items-center justify-between text-xs">
                <div>
                  <span className="font-bold text-slate-200">{it.event_type}</span>
                  <div className="text-[11px] text-brand-400 truncate max-w-xs">{it.product_name}</div>
                </div>
                <span className="text-[10px] text-slate-500">
                  {new Date(it.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
