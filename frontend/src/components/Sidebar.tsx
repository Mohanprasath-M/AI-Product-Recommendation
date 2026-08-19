import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  ShoppingBag, 
  Users, 
  Sparkles, 
  BarChart2, 
  MessageSquareText, 
  SearchCode, 
  Cpu, 
  Activity, 
  Settings,
  Heart,
  TrendingUp,
  Boxes
} from 'lucide-react';
import { useAuth } from '../auth/AuthContext';

export const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const role = user?.role || 'CUSTOMER';

  const customerNav = [
    { to: '/', label: 'Personalized For You', icon: Sparkles, badge: 'AI' },
    { to: '/products', label: 'Explore Catalog', icon: ShoppingBag },
    { to: '/customer/profile', label: 'My Intelligence Profile', icon: Users },
  ];

  const adminNav = [
    { to: '/admin', label: 'Executive Dashboard', icon: LayoutDashboard },
    { to: '/admin/products', label: 'Product Catalog Management', icon: Boxes },
    { to: '/admin/customers', label: 'Customer Directory & Risk', icon: Users },
    { to: '/admin/ml', label: 'MLOps & Model Registry', icon: Cpu, badge: 'Active' },
    { to: '/analyst/analytics', label: 'Conversion & Revenue', icon: BarChart2 },
  ];

  const analystNav = [
    { to: '/analyst', label: 'Customer Intelligence', icon: LayoutDashboard },
    { to: '/analyst/analytics', label: 'Funnel & Segments', icon: BarChart2 },
    { to: '/analyst/reviews', label: 'Review Sentiment NLP', icon: MessageSquareText, badge: 'NLP' },
    { to: '/analyst/search', label: 'Search Intelligence', icon: SearchCode },
    { to: '/admin/ml', label: 'Model Evaluation Metrics', icon: Cpu },
  ];

  const links = role === 'ADMIN' ? adminNav : (role === 'ANALYST' ? analystNav : customerNav);

  return (
    <aside className="w-64 shrink-0 hidden md:block border-r border-slate-800 bg-slate-950/40 p-4 min-h-[calc(100vh-4rem)]">
      <div className="space-y-6">
        
        {/* Navigation Section */}
        <div>
          <div className="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            {role === 'ADMIN' ? 'Admin Management' : (role === 'ANALYST' ? 'Analytics Suite' : 'AI Storefront')}
          </div>
          <nav className="space-y-1">
            {links.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink
                  key={link.to}
                  to={link.to}
                  end={link.to === '/' || link.to === '/admin' || link.to === '/analyst'}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                      isActive
                        ? 'bg-brand-600/20 text-brand-300 border border-brand-500/30 shadow-sm shadow-brand-500/10'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                    }`
                  }
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4" />
                    <span>{link.label}</span>
                  </div>
                  {link.badge && (
                    <span className="px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-300 border border-brand-500/30 text-[9px] font-bold">
                      {link.badge}
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* AI System Badge Card */}
        <div className="rounded-xl glass-card p-3.5 border border-slate-800/80 bg-gradient-to-b from-brand-950/20 to-slate-900/40">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="text-[11px] font-bold text-slate-200">Local ML Engine v1.0</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Running 100% locally with Hybrid TF-IDF, SVD Factorization, K-Means & NLP Sentiment without external API dependencies.
          </p>
        </div>

      </div>
    </aside>
  );
};
