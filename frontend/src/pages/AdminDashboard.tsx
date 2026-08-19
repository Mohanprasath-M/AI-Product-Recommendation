import React, { useState, useEffect } from 'react';
import { 
  DollarSign, 
  ShoppingBag, 
  Users, 
  TrendingUp, 
  Sparkles, 
  ShieldAlert, 
  Activity, 
  ArrowUpRight,
  RefreshCw,
  Layers
} from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { MetricCard } from '../components/MetricCard';
import { LiveStreamFeed } from '../components/LiveStreamFeed';
import { analyticsApi, eventsApi } from '../api/client';
import { OverviewKPIs, LiveActivityItem } from '../types';
import { useWebSocket } from '../hooks/useWebSocket';

export const AdminDashboard: React.FC = () => {
  const [kpis, setKpis] = useState<OverviewKPIs | null>(null);
  const [revenueTrends, setRevenueTrends] = useState<any[]>([]);
  const [categoryPerf, setCategoryPerf] = useState<any[]>([]);
  const [topProducts, setTopProducts] = useState<any[]>([]);
  const [atRiskCustomers, setAtRiskCustomers] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const { liveEvents, isConnected } = useWebSocket('admin');
  const [recentEvents, setRecentEvents] = useState<LiveActivityItem[]>([]);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const [k, rev, cat, top, risk, evs] = await Promise.all([
        analyticsApi.getOverview(),
        analyticsApi.getRevenueTrends(14),
        analyticsApi.getCategoryPerformance(),
        analyticsApi.getTopProducts(5),
        analyticsApi.getAtRiskCustomers(5),
        eventsApi.getLiveEvents(12)
      ]);
      setKpis(k);
      setRevenueTrends(rev || []);
      setCategoryPerf(cat || []);
      setTopProducts(top || []);
      setAtRiskCustomers(risk || []);
      setRecentEvents(evs || []);
    } catch (e) {
      console.error('Failed to load admin metrics:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const COLORS = ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#6366f1'];

  // Merge websocket live events with historical
  const displayedEvents = liveEvents.length > 0 ? [...liveEvents, ...recentEvents].slice(0, 15) : recentEvents;

  return (
    <div className="space-y-8 pb-16">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-bold uppercase tracking-wider">
              Executive View
            </span>
            <span className="text-xs text-slate-400 font-medium">PostgreSQL / MySQL Real-Time Store</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white mt-1">Platform Intelligence Overview</h1>
        </div>

        <button
          onClick={loadDashboardData}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-bold text-slate-200 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Analytics</span>
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <MetricCard
          title="Total Gross Revenue"
          value={`$${kpis?.total_revenue.toLocaleString() || '0'}`}
          change="+14.2% vs last month"
          isPositive={true}
          icon={DollarSign}
          color="brand"
        />
        <MetricCard
          title="Total Orders Completed"
          value={kpis?.total_orders.toLocaleString() || '0'}
          change="+8.6% week-over-week"
          isPositive={true}
          icon={ShoppingBag}
          color="cyan"
        />
        <MetricCard
          title="Active Customer Base"
          value={kpis?.active_customers.toLocaleString() || '0'}
          subtitle={`Out of ${kpis?.total_customers.toLocaleString() || '0'} registered`}
          icon={Users}
          color="emerald"
        />
        <MetricCard
          title="Recommendation CTR"
          value={`${kpis?.recommendation_ctr || '18.4'}%`}
          change={`${kpis?.recommendation_revenue_share || '32.6'}% AI Revenue Share`}
          isPositive={true}
          icon={Sparkles}
          color="amber"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Revenue Trends Chart */}
        <div className="lg:col-span-2 glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div>
              <h3 className="text-base font-bold text-white">Daily Revenue & Order Trajectory</h3>
              <p className="text-xs text-slate-400">14-day aggregated trend from completed purchases.</p>
            </div>
          </div>

          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueTrends}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                />
                <Area type="monotone" dataKey="revenue" stroke="#8b5cf6" strokeWidth={2.5} fillOpacity={1} fill="url(#colorRev)" name="Revenue ($)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Real-Time WebSocket Feed */}
        <LiveStreamFeed events={displayedEvents} maxItems={8} />

      </div>

      {/* Category Performance & Top Selling Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Category Breakdown */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div>
              <h3 className="text-base font-bold text-white">Category Revenue Contribution</h3>
              <p className="text-xs text-slate-400">Volume and conversion distribution across domains.</p>
            </div>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryPerf.slice(0, 6)} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis type="number" stroke="#64748b" fontSize={11} />
                <YAxis dataKey="category" type="category" stroke="#64748b" fontSize={10} width={90} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }} />
                <Bar dataKey="revenue" fill="#8b5cf6" radius={[0, 8, 8, 0]} name="Revenue ($)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Products Table */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div>
              <h3 className="text-base font-bold text-white">Top Performing Products</h3>
              <p className="text-xs text-slate-400">Ranked by revenue generated and purchase volume.</p>
            </div>
          </div>

          <div className="space-y-2.5">
            {topProducts.map((p) => (
              <div key={p.id} className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs">
                <div className="truncate max-w-xs">
                  <div className="font-bold text-slate-100 truncate">{p.name}</div>
                  <div className="text-[11px] text-slate-400">{p.category} • {p.purchases} sales</div>
                </div>
                <div className="text-right shrink-0">
                  <div className="font-extrabold text-emerald-400">${p.revenue.toLocaleString()}</div>
                  <div className="text-[10px] text-slate-400 font-semibold">{p.rating}★ rating</div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* At-Risk Customers Action Table */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-rose-400" />
            <div>
              <h3 className="text-base font-bold text-white">High-Value At-Risk Customers (Churn Alert)</h3>
              <p className="text-xs text-slate-400">Identified via statistical lapse and declining session velocity.</p>
            </div>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-bold uppercase tracking-wider">
                <th className="pb-3">Customer Name</th>
                <th className="pb-3">Historical Spend</th>
                <th className="pb-3">Days Inactive</th>
                <th className="pb-3">Risk Level</th>
                <th className="pb-3 text-right">Recommended Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {atRiskCustomers.map((c) => (
                <tr key={c.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-3 font-semibold text-slate-200">{c.name}</td>
                  <td className="py-3 text-slate-300 font-mono">${c.total_spend.toFixed(2)}</td>
                  <td className="py-3 text-slate-400">{c.days_since_last_active} days</td>
                  <td className="py-3">
                    <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-bold">
                      HIGH RISK ({(c.churn_risk_score * 100).toFixed(0)}%)
                    </span>
                  </td>
                  <td className="py-3 text-right">
                    <span className="text-[11px] font-bold text-brand-300 bg-brand-600/20 px-2.5 py-1 rounded-lg border border-brand-500/30">
                      Trigger Win-Back Voucher
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
