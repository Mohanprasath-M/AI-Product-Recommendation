import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './auth/AuthContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { CartDrawer } from './components/CartDrawer';
import { CustomerDashboard } from './pages/CustomerDashboard';
import { ProductCatalog } from './pages/ProductCatalog';
import { ProductDetail } from './pages/ProductDetail';
import { CustomerProfile } from './pages/CustomerProfile';
import { AdminDashboard } from './pages/AdminDashboard';
import { ProductManagement } from './pages/ProductManagement';
import { CustomerManagement } from './pages/CustomerManagement';
import { AnalystDashboard } from './pages/AnalystDashboard';
import { MLManagement } from './pages/MLManagement';
import { ReviewsNLP } from './pages/ReviewsNLP';
import { SearchIntelligence } from './pages/SearchIntelligence';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { ordersApi } from './api/client';
import { Product, CartItem } from './types';
import { useWebSocket } from './hooks/useWebSocket';

const MainLayout: React.FC = () => {
  const { user } = useAuth();
  const [cartOpen, setCartOpen] = useState(false);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const { isConnected } = useWebSocket(user?.id);

  const refreshCart = async () => {
    if (!user?.customer_id) return;
    try {
      const items = await ordersApi.getCart(user.customer_id);
      setCartItems(items || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    refreshCart();
  }, [user?.customer_id]);

  const handleAddToCart = async (product: Product) => {
    if (!user?.customer_id) {
      setCartOpen(true);
      return;
    }
    try {
      await ordersApi.addToCart(user.customer_id, product.id, 1);
      refreshCart();
      setCartOpen(true);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar
        cartCount={cartItems.reduce((sum, item) => sum + item.quantity, 0)}
        onOpenCart={() => setCartOpen(true)}
        isConnected={isConnected}
      />

      <div className="flex-1 max-w-7xl w-full mx-auto flex">
        <Sidebar />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 min-w-0">
          <Routes>
            <Route path="/" element={<CustomerDashboard onAddToCart={handleAddToCart} />} />
            <Route path="/products" element={<ProductCatalog onAddToCart={handleAddToCart} />} />
            <Route path="/products/:id" element={<ProductDetail onAddToCart={handleAddToCart} />} />
            <Route path="/customer/profile" element={<CustomerProfile />} />

            {/* Admin Routes */}
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/products" element={<ProductManagement />} />
            <Route path="/admin/customers" element={<CustomerManagement />} />
            <Route path="/admin/ml" element={<MLManagement />} />

            {/* Analyst Routes */}
            <Route path="/analyst" element={<AnalystDashboard />} />
            <Route path="/analyst/analytics" element={<AnalystDashboard />} />
            <Route path="/analyst/reviews" element={<ReviewsNLP />} />
            <Route path="/analyst/search" element={<SearchIntelligence />} />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>

      <CartDrawer
        isOpen={cartOpen}
        onClose={() => setCartOpen(false)}
        cartItems={cartItems}
        onRefreshCart={refreshCart}
      />
    </div>
  );
};

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/*" element={<MainLayout />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
