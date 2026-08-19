import React, { useState, useEffect } from 'react';
import { 
  BarChart2, 
  Layers, 
  Users, 
  Activity, 
  PieChart as PieIcon, 
  RefreshCw,
  TrendingUp,
  Sliders
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';
import { analyticsApi, customersApi } from '../api/client';
import { CustomerSegment } from '../types';

export const AnalystDashboard: React.FC = () => {
  const [funnel, setFunnel] = useState<any>(null);
  const [segments, setSegments] = useState<CustomerSegment[]>([]);
  const [categoryPerf, setCategoryPerf] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [f, s, c] = await Promise.all([
        analyticsApi.getConversionFunnel(),
        customersApi.getSegments(),
        analyticsApi.getCategoryPerformance()
      ]);
      setFunnel(f);
      setSegments(s || []);
      setCategoryPerf(c || []);
    } catch (e) {
      console.error('Failed to load analyst analytics:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const COLORS = ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#3b82f6'];

  const funnelData = funnel ? [
    { stage: '1. Searches', count: funnel.searches, fill: '#6366f1' },
    { stage: '2. Product Views', count: funnel.views, fill: '#8b5cf6' },
    { stage: '3. Clicks', count: funnel.clicks, fill: '#a855f7' },
    { stage: '4. Cart Additions', count: funnel.carts, fill: '#06b6d4' },
    { stage: '5. Purchases', count: funnel.purchases, fill: '#10b981' }
  ] : [];

  return (
    <div className="space-y-8 pb-16">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-bold uppercase tracking-wider">
              Analyst Suite
            </span>
            <span className="text-xs text-slate-400 font-medium">Customer Intelligence & Funnels</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white mt-1">Behavioral Segmentation & Conversion Analytics</h1>
        </div>

        <button
          onClick={loadData}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-bold text-slate-200 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Data</span>
        </button>
      </div>

      {/* Conversion Funnel Stage Cards */}
      {funnel && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          <div className="glass-card rounded-2xl p-4 border border-slate-800">
            <div className="text-xs font-bold text-slate-400 uppercase">Search Ingestion</div>
            <div className="text-xl font-black text-white mt-1">{funnel.searches.toLocaleString()}</div>
            <div className="text-[11px] text-slate-500 mt-1">Queries tracked</div>
          </div>
          <div className="glass-card rounded-2xl p-4 border border-slate-800">
            <div className="text-xs font-bold text-slate-400 uppercase">Catalog Views</div>
            <div className="text-xl font-black text-white mt-1">{funnel.views.toLocaleString()}</div>
            <div className="text-[11px] text-brand-400 mt-1">Primary browsing pool</div>
          </div>
          <div className="glass-card rounded-2xl p-4 border border-slate-800">
            <div className="text-xs font-bold text-slate-400 uppercase">Cart Additions</div>
            <div className="text-xl font-black text-white mt-1">{funnel.carts.toLocaleString()}</div>
            <div className="text-[11px] text-cyan-400 mt-1">{funnel.view_to_cart_pct}% View-to-Cart</div>
          </div>
          <div className="glass-card rounded-2xl p-4 border border-slate-800">
            <div className="text-xs font-bold text-slate-400 uppercase">Purchases</div>
            <div className="text-xl font-black text-emerald-400 mt-1">{funnel.purchases.toLocaleString()}</div>
            <div className="text-[11px] text-emerald-400 font-semibold">{funnel.cart_to_purchase_pct}% Cart-to-Buy</div>
          </div>
          <div className="glass-card rounded-2xl p-4 border border-slate-800">
            <div className="text-xs font-bold text-slate-400 uppercase">Overall Conversion</div>
            <div className="text-xl font-black text-brand-300 mt-1">{funnel.overall_conversion_pct}%</div>
            <div className="text-[11px] text-slate-400 mt-1">End-to-End conversion</div>
          </div>
        </div>
      )}

      {/* Main Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Full Funnel Bar Chart */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="pb-2 border-b border-slate-800">
            <h3 className="text-base font-bold text-white">Full-Funnel Conversion Dropoff</h3>
            <p className="text-xs text-slate-400">Step-by-step customer volume decay across user actions.</p>
          </div>

          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnelData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="stage" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }} />
                <Bar dataKey="count" radius={[8, 8, 0, 0]} name="Events Count">
                  {funnelData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Customer Segmentation Pie Chart */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="pb-2 border-b border-slate-800">
            <h3 className="text-base font-bold text-white">K-Means Customer Segmentation Clusters</h3>
            <p className="text-xs text-slate-400">Persona distribution derived from spend, cadence, and recency.</p>
          </div>

          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={segments}
                  dataKey="customer_count"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={90}
                  innerRadius={45}
                  paddingAngle={3}
                >
                  {segments.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Cluster Persona Profiles Table */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
        <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
          <Users className="w-5 h-5 text-brand-400" />
          <div>
            <h3 className="text-base font-bold text-white">Segment Cluster Profiles & Behavioral Characteristics</h3>
            <p className="text-xs text-slate-400">Automated persona definitions generated by the K-Means clustering engine.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {segments.map((seg, i) => (
            <div key={seg.id} className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-brand-300 bg-brand-500/20 px-2.5 py-1 rounded-lg border border-brand-500/30">
                  Cluster {seg.cluster_index + 1}
                </span>
                <span className="text-xs text-slate-400 font-semibold">{seg.customer_count} Shoppers</span>
              </div>

              <div className="font-extrabold text-sm text-white">{seg.name}</div>

              <div className="space-y-1 text-xs text-slate-300 pt-2 border-t border-slate-800/80">
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Spending:</span>
                  <span className="font-bold text-white">${seg.avg_spending.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Avg Order Value:</span>
                  <span className="font-bold text-white">${seg.avg_order_value.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Purchase Frequency:</span>
                  <span className="font-bold text-white">{seg.avg_purchase_frequency} orders</span>
                </div>
              </div>

              {seg.key_characteristics && seg.key_characteristics.length > 0 && (
                <div className="pt-2 border-t border-slate-800/80 space-y-1">
                  {seg.key_characteristics.map((trait, t_idx) => (
                    <div key={t_idx} className="text-[11px] text-slate-400 flex items-center gap-1.5">
                      <span className="w-1 h-1 rounded-full bg-brand-400 shrink-0" />
                      <span>{trait}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
