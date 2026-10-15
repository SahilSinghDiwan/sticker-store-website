import { useState, useEffect } from "react";
import { api } from "../lib/api.ts";

interface OrderItem {
  product: {
    _id: string;
    name: string;
    price: number;
  };
  quantity: number;
}

interface Order {
  _id: string;
  items: OrderItem[];
  total: number;
  status: "pending" | "processing" | "shipped" | "delivered";
  createdAt: string;
  trackingNumber?: string;
}

export default function OrderHistory() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await api.get("/orders");
        const data = response.data as { orders: Order[] };
        setOrders(data.orders);
      } catch (error) {
        console.error("Failed to fetch orders:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  if (loading) {
    return (
      <p className="text-[var(--color-ink-2)] font-mono text-[var(--text-sm)]">
        Loading orders…
      </p>
    );
  }

  return (
    <div className="max-w-3xl">
      <h1 className="font-display text-[length:var(--text-display-s)] m-0 mb-[var(--space-lg)]">
        Orders
      </h1>

      <div className="space-y-[var(--space-md)]">
        {orders.length === 0 ? (
          <p className="text-[var(--color-ink-2)] py-[var(--space-xl)] border-t border-[var(--color-rule)]">
            No orders yet.
          </p>
        ) : (
          orders.map((order) => (
            <article
              key={order._id}
              className="border border-[var(--color-rule)] rounded-[var(--radius-card)] p-[var(--space-md)]"
            >
              <div className="flex justify-between items-start gap-[var(--space-sm)] mb-[var(--space-sm)]">
                <div>
                  <p className="font-mono text-[var(--text-xs)] text-[var(--color-ink-2)] m-0">
                    #{order._id.slice(-8)}
                  </p>
                  <p className="font-mono text-[var(--text-xs)] text-[var(--color-ink-2)] m-0 mt-1">
                    {new Date(order.createdAt).toLocaleDateString()}
                  </p>
                </div>
                <span className="font-mono text-[var(--text-xs)] uppercase tracking-wide text-[var(--color-accent)]">
                  {order.status}
                </span>
              </div>

              <div className="border-t border-[var(--color-rule)] pt-[var(--space-sm)]">
                {order.items.map((item, index) => (
                  <div
                    key={index}
                    className="flex justify-between gap-4 py-[var(--space-2xs)]"
                  >
                    <div className="min-w-0">
                      <p className="font-display m-0 truncate">
                        {item.product.name}
                      </p>
                      <p className="font-mono text-[var(--text-xs)] text-[var(--color-ink-2)] m-0">
                        Qty {item.quantity}
                      </p>
                    </div>
                    <p className="price m-0 shrink-0">
                      ${(item.product.price * item.quantity).toFixed(2)}
                    </p>
                  </div>
                ))}
              </div>

              <div className="border-t border-[var(--color-rule)] mt-[var(--space-sm)] pt-[var(--space-sm)] flex justify-between">
                <p className="font-mono text-[var(--text-xs)] uppercase m-0 text-[var(--color-ink-2)]">
                  Total
                </p>
                <p className="price font-medium m-0">
                  ${order.total.toFixed(2)}
                </p>
              </div>

              {order.trackingNumber && (
                <p className="font-mono text-[var(--text-xs)] text-[var(--color-ink-2)] mt-[var(--space-sm)] mb-0">
                  Tracking {order.trackingNumber}
                </p>
              )}
            </article>
          ))
        )}
      </div>
    </div>
  );
}
