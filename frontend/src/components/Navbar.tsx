import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  Search, 
  ShoppingCart, 
  User as UserIcon, 
  LogOut, 
  Shield, 
  BarChart3, 
  Activity, 
  Radio,
  SlidersHorizontal,
  ChevronDown
} from 'lucide-react';
import { useAuth } from '../auth/AuthContext';
import { eventsApi } from '../api/client';

interface NavbarProps {
  cartCount?: number;
  onOpenCart?: () => void;
  isConnected?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ cartCount = 0, onOpenCart, isConnected = true }) => {
  const { user, logout, switchDemoRole } = useAuth();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [roleDropdownOpen, setRoleDropdownOpen] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    eventsApi.trackSearch(searchQuery, user?.customer_id);
    navigate(`/products?search=${encodeURIComponent(searchQuery.trim())}`);
  };

  return (
    <header className="sticky top-0 z-40 border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2.5 group shrink-0">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-brand-500/20 group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-brand-300 bg-clip-text text-transparent">
                NexusAI
              </span>
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-300 border border-brand-500/30 font-semibold tracking-wider uppercase">
                Enterprise
              </span>
            </div>
            <p className="text-[10px] text-slate-400 font-medium leading-none">Recommendation & Customer Intelligence</p>
          </div>
        </Link>

        {/* Global Search Bar */}
        <form onSubmit={handleSearch} className="flex-1 max-w-md hidden md:block">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search products, brands, or AI features..."
              className="w-full bg-slate-900/90 border border-slate-800 focus:border-brand-500 rounded-xl pl-10 pr-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500/50 transition-all"
            />
          </div>
        </form>

        {/* Action Controls & Role Switcher */}
        <div className="flex items-center gap-3">
          
          {/* Real-time WebSocket Live Status */}
          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs">
            <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
            <span className="text-slate-300 text-[11px] font-medium">
              {isConnected ? 'Real-Time Stream Active' : 'Connecting'}
            </span>
          </div>

          {/* Quick Role Switcher (Admin / Analyst / Customer) */}
          <div className="relative">
            <button
              onClick={() => setRoleDropdownOpen(!roleDropdownOpen)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-semibold text-slate-200 transition-colors"
            >
              {user?.role === 'ADMIN' && <Shield className="w-3.5 h-3.5 text-amber-400" />}
              {user?.role === 'ANALYST' && <BarChart3 className="w-3.5 h-3.5 text-cyan-400" />}
              {user?.role === 'CUSTOMER' && <UserIcon className="w-3.5 h-3.5 text-brand-400" />}
              <span>{user?.role || 'Switch Role'}</span>
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </button>

            {roleDropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 rounded-xl glass-card p-1.5 shadow-2xl z-50 animate-in fade-in slide-in-from-top-2">
                <div className="px-2.5 py-1 text-[10px] font-semibold tracking-wider text-slate-400 uppercase">
                  Switch User Persona
                </div>
                <button
                  onClick={() => { switchDemoRole('CUSTOMER'); setRoleDropdownOpen(false); }}
                  className={`w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-xs font-medium text-left transition-colors ${
                    user?.role === 'CUSTOMER' ? 'bg-brand-600/30 text-brand-300 font-semibold' : 'text-slate-300 hover:bg-slate-800'
                  }`}
                >
                  <UserIcon className="w-4 h-4 text-brand-400" />
                  <div>
                    <div>Customer Storefront</div>
                    <div className="text-[10px] text-slate-400">Personalized Feed</div>
                  </div>
                </button>
                <button
                  onClick={() => { switchDemoRole('ADMIN'); setRoleDropdownOpen(false); }}
                  className={`w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-xs font-medium text-left transition-colors ${
                    user?.role === 'ADMIN' ? 'bg-brand-600/30 text-brand-300 font-semibold' : 'text-slate-300 hover:bg-slate-800'
                  }`}
                >
                  <Shield className="w-4 h-4 text-amber-400" />
                  <div>
                    <div>Admin Portal</div>
                    <div className="text-[10px] text-slate-400">Products, MLOps, Rules</div>
                  </div>
                </button>
                <button
                  onClick={() => { switchDemoRole('ANALYST'); setRoleDropdownOpen(false); }}
                  className={`w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-xs font-medium text-left transition-colors ${
                    user?.role === 'ANALYST' ? 'bg-brand-600/30 text-brand-300 font-semibold' : 'text-slate-300 hover:bg-slate-800'
                  }`}
                >
                  <BarChart3 className="w-4 h-4 text-cyan-400" />
                  <div>
                    <div>Analyst Intelligence</div>
                    <div className="text-[10px] text-slate-400">CLV, NLP, Segments</div>
                  </div>
                </button>
              </div>
            )}
          </div>

          {/* Cart Trigger */}
          {user?.role === 'CUSTOMER' && (
            <button
              onClick={onOpenCart}
              className="relative p-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white transition-colors"
              title="Shopping Cart"
            >
              <ShoppingCart className="w-5 h-5" />
              {cartCount > 0 && (
                <span className="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-brand-600 text-white text-[11px] font-bold flex items-center justify-center glow-badge">
                  {cartCount}
                </span>
              )}
            </button>
          )}

          {/* User Profile */}
          <div className="flex items-center gap-2 border-l border-slate-800 pl-3">
            <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-bold text-slate-200">
              {user?.full_name?.charAt(0) || 'U'}
            </div>
            <div className="hidden lg:block text-left text-xs leading-tight">
              <div className="font-semibold text-slate-200 truncate max-w-[120px]">{user?.full_name}</div>
              <div className="text-[10px] text-slate-400">{user?.role}</div>
            </div>
            <button
              onClick={logout}
              className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-rose-400 transition-colors"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
