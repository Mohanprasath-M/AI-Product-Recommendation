import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Search, 
  Filter, 
  ShieldAlert, 
  Sparkles, 
  DollarSign, 
  ChevronRight,
  TrendingUp,
  X
} from 'lucide-react';
import { customersApi } from '../api/client';
import { Customer, CustomerSegment } from '../types';

export const CustomerManagement: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [segments, setSegments] = useState<CustomerSegment[]>([]);
  const [search, setSearch] = useState('');
  const [selectedSegment, setSelectedSegment] = useState('');
  const [selectedRisk, setSelectedRisk] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);

  const loadCustomers = async () => {
    setIsLoading(true);
    try {
      const [custData, segData] = await Promise.all([
        customersApi.list({
          page,
          size: 10,
          search: search || undefined,
          segment_id: selectedSegment || undefined,
          churn_risk_level: selectedRisk || undefined
        }),
        customersApi.getSegments()
      ]);
      setCustomers(custData.items || []);
      setTotalPages(custData.pages || 1);
      setTotalCount(custData.total || 0);
      setSegments(segData || []);
    } catch (e) {
      console.error('Failed to load customers:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCustomers();
  }, [search, selectedSegment, selectedRisk, page]);

  return (
    <div className="space-y-6 pb-16">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-black text-white">Customer Directory & Churn Risk</h1>
        <p className="text-xs text-slate-400 mt-1">
          {totalCount} total customer profiles enriched with K-Means segmentation and lifetime value calculations.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="glass-card rounded-2xl p-4 border border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search customer by name, email, code..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>

        <select
          value={selectedSegment}
          onChange={(e) => setSelectedSegment(e.target.value)}
          className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-300 focus:outline-none"
        >
          <option value="">All Behavioral Clusters</option>
          {segments.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>

        <select
          value={selectedRisk}
          onChange={(e) => setSelectedRisk(e.target.value)}
          className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-300 focus:outline-none"
        >
          <option value="">All Risk Profiles</option>
          <option value="HIGH">High Churn Risk</option>
          <option value="MEDIUM">Medium Churn Risk</option>
          <option value="LOW">Low Churn Risk</option>
        </select>
      </div>

      {/* Customers Table */}
      <div className="glass-card rounded-3xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 border-b border-slate-800 text-slate-400 font-bold uppercase tracking-wider">
              <tr>
                <th className="p-4">Customer</th>
                <th className="p-4">Persona / Segment</th>
                <th className="p-4">Total Spend</th>
                <th className="p-4">Orders</th>
                <th className="p-4">Estimated CLV</th>
                <th className="p-4">Churn Risk</th>
                <th className="p-4 text-right">Profile</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {customers.map((c) => (
                <tr key={c.id} className="hover:bg-slate-900/40 transition-colors">
                  <td className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center font-bold text-slate-300">
                        {c.name.charAt(0)}
                      </div>
                      <div>
                        <div className="font-bold text-slate-100">{c.name}</div>
                        <div className="text-[11px] text-slate-500 font-mono">{c.customer_code} • {c.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="p-4">
                    <span className="px-2.5 py-1 rounded-lg bg-brand-500/20 text-brand-300 border border-brand-500/30 text-[11px] font-semibold">
                      {c.segment_name || c.persona}
                    </span>
                  </td>
                  <td className="p-4 font-mono font-bold text-white">${c.total_spend.toFixed(2)}</td>
                  <td className="p-4 text-slate-300">{c.total_orders}</td>
                  <td className="p-4 font-mono font-extrabold text-brand-300">${c.clv_estimated.toFixed(2)}</td>
                  <td className="p-4">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                      c.churn_risk_level === 'HIGH'
                        ? 'bg-rose-500/20 text-rose-300 border-rose-500/30'
                        : c.churn_risk_level === 'MEDIUM'
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/30'
                        : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                    }`}>
                      {c.churn_risk_level} ({(c.churn_risk_score * 100).toFixed(0)}%)
                    </span>
                  </td>
                  <td className="p-4 text-right">
                    <button
                      onClick={() => setSelectedCustomer(c)}
                      className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold transition-colors"
                    >
                      Inspect
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Customer Quick Inspect Modal */}
      {selectedCustomer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900 max-w-md w-full space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white">Customer Profile Inspector</h3>
              <button onClick={() => setSelectedCustomer(null)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1">
                <div className="font-extrabold text-sm text-white">{selectedCustomer.name}</div>
                <div className="text-slate-400">{selectedCustomer.email}</div>
                <div className="text-slate-500">{selectedCustomer.location} • Age {selectedCustomer.age}</div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-slate-400">Fav Category</div>
                  <div className="font-bold text-slate-200 mt-0.5">{selectedCustomer.favorite_category || 'Electronics'}</div>
                </div>
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-slate-400">Fav Brand</div>
                  <div className="font-bold text-slate-200 mt-0.5">{selectedCustomer.favorite_brand || 'Sony'}</div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-slate-400">Average Order Value:</span>
                  <span className="font-bold text-white">${selectedCustomer.avg_order_value.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Estimated 1-Year CLV:</span>
                  <span className="font-bold text-brand-300">${selectedCustomer.clv_estimated.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Churn Risk Level:</span>
                  <span className="font-bold text-rose-400">{selectedCustomer.churn_risk_level}</span>
                </div>
              </div>
            </div>

            <button
              onClick={() => setSelectedCustomer(null)}
              className="w-full py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold"
            >
              Close Inspector
            </button>
          </div>
        </div>
      )}

    </div>
  );
};
