import React, { useState } from 'react';
import { X, Trash2, ShoppingBag, ArrowRight, CheckCircle2 } from 'lucide-react';
import { CartItem } from '../types';
import { ordersApi } from '../api/client';
import { useAuth } from '../auth/AuthContext';

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  cartItems: CartItem[];
  onRefreshCart: () => void;
}

export const CartDrawer: React.FC<CartDrawerProps> = ({
  isOpen,
  onClose,
  cartItems,
  onRefreshCart
}) => {
  const { user } = useAuth();
  const [isCheckingOut, setIsCheckingOut] = useState(false);
  const [orderSuccess, setOrderSuccess] = useState<string | null>(null);

  if (!isOpen) return null;

  const totalAmount = cartItems.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0);

  const handleRemove = async (productId: string) => {
    if (!user?.customer_id) return;
    await ordersApi.removeFromCart(user.customer_id, productId);
    onRefreshCart();
  };

  const handleCheckout = async () => {
    if (!user?.customer_id || cartItems.length === 0) return;
    setIsCheckingOut(true);
    try {
      const itemsPayload = cartItems.map(item => ({
        product_id: item.product_id,
        quantity: item.quantity
      }));
      const order = await ordersApi.checkout(user.customer_id, itemsPayload);
      setOrderSuccess(order.order_code);
      onRefreshCart();
    } catch (e) {
      console.error('Checkout error:', e);
    } finally {
      setIsCheckingOut(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity" onClick={onClose} />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col justify-between">
          
          {/* Header */}
          <div className="p-5 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <ShoppingBag className="w-5 h-5 text-brand-400" />
              <h2 className="text-base font-extrabold text-white">Your Shopping Cart</h2>
              <span className="px-2 py-0.5 rounded-full bg-slate-800 text-xs font-semibold text-slate-300">
                {cartItems.length}
              </span>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Cart Item List */}
          <div className="p-5 flex-1 overflow-y-auto space-y-4">
            {orderSuccess ? (
              <div className="text-center py-12 space-y-3">
                <div className="w-14 h-14 mx-auto rounded-2xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h3 className="text-lg font-bold text-white">Order Confirmed!</h3>
                <p className="text-xs text-slate-400">
                  Order Code: <span className="font-mono font-bold text-brand-400">{orderSuccess}</span>
                </p>
                <p className="text-xs text-slate-500">
                  Real-time events and recommendation weights updated across all dashboards.
                </p>
                <button
                  onClick={() => { setOrderSuccess(null); onClose(); }}
                  className="mt-4 px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold transition-colors"
                >
                  Continue Exploring
                </button>
              </div>
            ) : cartItems.length === 0 ? (
              <div className="text-center py-16 space-y-2">
                <ShoppingBag className="w-12 h-12 mx-auto text-slate-600" />
                <p className="text-sm font-semibold text-slate-400">Your cart is empty</p>
                <p className="text-xs text-slate-500">Browse recommendations to add items.</p>
              </div>
            ) : (
              cartItems.map((item) => (
                <div
                  key={item.id}
                  className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 flex items-center justify-between gap-3"
                >
                  <div className="w-12 h-12 rounded-lg bg-slate-900 flex items-center justify-center p-1 shrink-0">
                    <img
                      src={item.product?.image_url || "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"}
                      alt={item.product?.name}
                      className="object-contain max-h-full"
                    />
                  </div>

                  <div className="flex-1 min-w-0">
                    <h4 className="text-xs font-bold text-slate-200 truncate">{item.product?.name}</h4>
                    <div className="text-[11px] text-slate-400 mt-0.5">
                      Qty: {item.quantity} × ${item.unit_price.toFixed(2)}
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-xs font-extrabold text-white">
                      ${(item.quantity * item.unit_price).toFixed(2)}
                    </div>
                    <button
                      onClick={() => handleRemove(item.product_id)}
                      className="text-slate-500 hover:text-rose-400 p-1 transition-colors"
                      title="Remove"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer & Checkout */}
          {!orderSuccess && cartItems.length > 0 && (
            <div className="p-5 border-t border-slate-800 bg-slate-950/50 space-y-4">
              <div className="space-y-1.5 text-xs">
                <div className="flex justify-between text-slate-400">
                  <span>Subtotal</span>
                  <span>${totalAmount.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Estimated Tax (8%)</span>
                  <span>${(totalAmount * 0.08).toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm font-extrabold text-white pt-2 border-t border-slate-800">
                  <span>Total</span>
                  <span className="text-brand-300">${(totalAmount * 1.08).toFixed(2)}</span>
                </div>
              </div>

              <button
                onClick={handleCheckout}
                disabled={isCheckingOut}
                className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white text-xs font-bold shadow-lg shadow-brand-600/30 transition-all disabled:opacity-50"
              >
                {isCheckingOut ? (
                  <span>Processing Real-Time Order...</span>
                ) : (
                  <>
                    <span>Complete Purchase Flow</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};
