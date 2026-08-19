import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, Shield, BarChart3, User, ArrowRight } from 'lucide-react';
import { useAuth } from '../auth/AuthContext';

export const Login: React.FC = () => {
  const { login, switchDemoRole } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('customer@platform.ai');
  const [password, setPassword] = useState('Customer@123456');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await login(email, password);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickLogin = async (role: 'ADMIN' | 'ANALYST' | 'CUSTOMER') => {
    await switchDemoRole(role);
    if (role === 'ADMIN') navigate('/admin');
    else if (role === 'ANALYST') navigate('/analyst');
    else navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950">
      <div className="max-w-md w-full glass-card rounded-3xl p-8 border border-slate-800 bg-slate-900/60 space-y-6 shadow-2xl">
        
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center mx-auto shadow-xl shadow-brand-500/20">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-black text-white">Sign in to NexusAI</h1>
          <p className="text-xs text-slate-400">Enterprise AI Product Recommendation & Customer Intelligence</p>
        </div>

        {/* 1-Click Demo Persona Switcher */}
        <div className="p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block text-center">
            ⚡ Quick 1-Click Persona Login
          </span>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => handleQuickLogin('CUSTOMER')}
              className="p-2 rounded-xl bg-slate-900 hover:bg-brand-600/30 text-brand-300 border border-brand-500/30 text-xs font-bold transition-colors flex flex-col items-center gap-1"
            >
              <User className="w-4 h-4" />
              <span>Customer</span>
            </button>
            <button
              onClick={() => handleQuickLogin('ADMIN')}
              className="p-2 rounded-xl bg-slate-900 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 text-xs font-bold transition-colors flex flex-col items-center gap-1"
            >
              <Shield className="w-4 h-4" />
              <span>Admin</span>
            </button>
            <button
              onClick={() => handleQuickLogin('ANALYST')}
              className="p-2 rounded-xl bg-slate-900 hover:bg-cyan-600/30 text-cyan-300 border border-cyan-500/30 text-xs font-bold transition-colors flex flex-col items-center gap-1"
            >
              <BarChart3 className="w-4 h-4" />
              <span>Analyst</span>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          {error && (
            <div className="p-3 rounded-xl bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-semibold">
              {error}
            </div>
          )}

          <div>
            <label className="block text-slate-300 font-semibold mb-1">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white focus:outline-none focus:border-brand-500"
              required
            />
          </div>

          <div>
            <label className="block text-slate-300 font-semibold mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white focus:outline-none focus:border-brand-500"
              required
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-bold transition-all shadow-lg shadow-brand-600/30 disabled:opacity-50"
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="text-center text-xs text-slate-400">
          Don't have an account?{' '}
          <Link to="/register" className="text-brand-400 font-bold hover:underline">
            Register now
          </Link>
        </div>

      </div>
    </div>
  );
};
