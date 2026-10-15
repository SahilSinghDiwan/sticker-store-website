import { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "./ui/button";

interface CartItem {
  _id: string;
  name: string;
  price: number;
  quantity: number;
  image_url: string;
}

export default function Cart() {
  const [items, setItems] = useState<CartItem[]>([]);

  const updateQuantity = (id: string, newQuantity: number) => {
    if (newQuantity < 1) return;
    setItems(
      items.map((item) =>
        item._id === id ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  const removeItem = (id: string) => {
    setItems(items.filter((item) => item._id !== id));
  };

  const total = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  return (
    <div className="max-w-3xl">
      <h1 className="font-display text-[length:var(--text-display-s)] m-0 mb-[var(--space-lg)]">
        Cart
      </h1>

      {items.length === 0 ? (
        <div className="py-[var(--space-xl)] border-t border-[var(--color-rule)]">
          <p className="text-[var(--color-ink-2)] mb-[var(--space-md)]">
            Your cart is empty.
          </p>
          <Link to="/">
            <Button>Continue shopping</Button>
          </Link>
        </div>
      ) : (
        <>
          <ul className="list-none m-0 p-0 divide-y divide-[var(--color-rule)] border-y border-[var(--color-rule)]">
            {items.map((item) => (
              <li
                key={item._id}
                className="flex flex-wrap items-center gap-[var(--space-sm)] py-[var(--space-md)]"
              >
                <img
                  src={item.image_url}
                  alt={item.name}
                  className="w-16 h-16 object-cover rounded-[var(--radius-card)] border border-[var(--color-rule)]"
                />
                <div className="flex-grow min-w-0">
                  <h3 className="font-display text-[length:var(--text-md)] m-0 truncate">
                    {item.name}
                  </h3>
                  <p className="price text-[var(--color-ink-2)] m-0 mt-1">
                    ${item.price.toFixed(2)}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => updateQuantity(item._id, item.quantity - 1)}
                    aria-label="Decrease quantity"
                  >
                    −
                  </Button>
                  <span className="price w-8 text-center">{item.quantity}</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => updateQuantity(item._id, item.quantity + 1)}
                    aria-label="Increase quantity"
                  >
                    +
                  </Button>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeItem(item._id)}
                >
                  Remove
                </Button>
              </li>
            ))}
          </ul>

          <div className="mt-[var(--space-lg)] flex flex-wrap items-center justify-between gap-[var(--space-md)]">
            <div>
              <span className="font-mono text-[var(--text-xs)] uppercase tracking-wide text-[var(--color-ink-2)]">
                Total
              </span>
              <p className="price text-[length:var(--text-xl)] font-medium m-0">
                ${total.toFixed(2)}
              </p>
            </div>
            <Link to="/checkout">
              <Button size="lg">Checkout</Button>
            </Link>
          </div>
        </>
      )}
    </div>
  );
}
