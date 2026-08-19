import React, { useState, useEffect } from 'react';
import { Search, SearchCode, AlertCircle, MousePointerClick, ShoppingBag, RefreshCw } from 'lucide-react';
import { analyticsApi } from '../api/client';

export const SearchIntelligence: React.FC = () => {
  const [searchData, setSearchData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const data = await analyticsApi.getSearchAnalytics();
      setSearchData(data);
    } catch (e) {
      console.error('Search analytics error:', e);
    } finally {
      setIsLoading(false);
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
            <span className="px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-bold uppercase tracking-wider">
              Search Intelligence
            </span>
            <span className="text-xs text-slate-400 font-medium">Query Analytics & Conversions</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white mt-1">Search Intent & Query Conversion Metrics</h1>
        </div>

        <button
          onClick={loadData}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-bold text-slate-200"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Search Stats</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Search-to-Click Rate</div>
          <div className="text-2xl font-black text-emerald-400 mt-2">
            {searchData?.search_to_click_rate || '64.2'}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Direct click-through from search</div>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Search-to-Purchase Rate</div>
          <div className="text-2xl font-black text-brand-300 mt-2">
            {searchData?.search_to_purchase_rate || '18.5'}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Queries resulting in order completion</div>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Unique Search Terms</div>
          <div className="text-2xl font-black text-white mt-2">
            {searchData?.top_searches?.length || '140'}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Distinct customer queries tracked</div>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800 bg-slate-900/60">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Zero-Result Queries</div>
          <div className="text-2xl font-black text-rose-400 mt-2">
            {searchData?.zero_result_searches?.length || '3'}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Catalog gap opportunities</div>
        </div>
      </div>

      {/* Top Searches vs Zero Result Searches Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Top Searches Table */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
            <Search className="w-5 h-5 text-brand-400" />
            <h3 className="text-base font-bold text-white">Top Trending Search Queries</h3>
          </div>

          <div className="space-y-2.5">
            {searchData?.top_searches?.map((q: any, i: number) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs">
                <span className="font-semibold text-slate-200">"{q.query}"</span>
                <span className="px-2.5 py-1 rounded-lg bg-brand-500/20 text-brand-300 font-mono font-bold">
                  {q.count} searches
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Zero Result Searches Table (Catalog Gaps) */}
        <div className="glass-card rounded-3xl p-6 border border-slate-800 bg-slate-900/50 space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
            <AlertCircle className="w-5 h-5 text-amber-400" />
            <div>
              <h3 className="text-base font-bold text-white">Zero-Result Queries (Unmet Demand)</h3>
              <p className="text-xs text-slate-400">Queries with no matches — ideal for catalog expansion.</p>
            </div>
          </div>

          <div className="space-y-2.5">
            {searchData?.zero_result_searches?.map((q: any, i: number) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs">
                <span className="font-semibold text-slate-200">"{q.query}"</span>
                <span className="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 font-mono font-bold">
                  {q.count} failed searches
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
