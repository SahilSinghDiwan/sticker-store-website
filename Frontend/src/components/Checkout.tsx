import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";

interface ShippingAddress {
  street: string;
  city: string;
  state: string;
  zip: string;
  country: string;
}

export default function Checkout() {
  const navigate = useNavigate();
  const [address, setAddress] = useState<ShippingAddress>({
    street: "",
    city: "",
    state: "",
    zip: "",
    country: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/orders");
  };

  return (
    <div className="max-w-xl">
      <h1 className="font-display text-[length:var(--text-display-s)] m-0 mb-[var(--space-lg)]">
        Checkout
      </h1>

      <form onSubmit={handleSubmit} className="space-y-[var(--space-lg)]">
        <section className="border border-[var(--color-rule)] rounded-[var(--radius-card)] p-[var(--space-md)]">
          <h2 className="font-display text-[length:var(--text-lg)] m-0 mb-[var(--space-md)]">
            Shipping
          </h2>
          <div className="field">
            <label htmlFor="street">Street</label>
            <input
              id="street"
              type="text"
              value={address.street}
              onChange={(e) =>
                setAddress((prev) => ({ ...prev, street: e.target.value }))
              }
              required
            />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-[var(--space-sm)]">
            <div className="field">
              <label htmlFor="city">City</label>
              <input
                id="city"
                type="text"
                value={address.city}
                onChange={(e) =>
                  setAddress((prev) => ({ ...prev, city: e.target.value }))
                }
                required
              />
            </div>
            <div className="field">
              <label htmlFor="state">State</label>
              <input
                id="state"
                type="text"
                value={address.state}
                onChange={(e) =>
                  setAddress((prev) => ({ ...prev, state: e.target.value }))
                }
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-[var(--space-sm)]">
            <div className="field">
              <label htmlFor="zip">ZIP</label>
              <input
                id="zip"
                type="text"
                value={address.zip}
                onChange={(e) =>
                  setAddress((prev) => ({ ...prev, zip: e.target.value }))
                }
                required
              />
            </div>
            <div className="field">
              <label htmlFor="country">Country</label>
              <input
                id="country"
                type="text"
                value={address.country}
                onChange={(e) =>
                  setAddress((prev) => ({ ...prev, country: e.target.value }))
                }
                required
              />
            </div>
          </div>
        </section>

        <section className="border border-[var(--color-rule)] rounded-[var(--radius-card)] p-[var(--space-md)]">
          <h2 className="font-display text-[length:var(--text-lg)] m-0 mb-[var(--space-md)]">
            Payment
          </h2>
          <div className="min-h-28 flex items-center justify-center border border-dashed border-[var(--color-rule)] rounded-[var(--radius-card)] px-[var(--space-md)]">
            <p className="text-[var(--color-ink-2)] text-[var(--text-sm)] m-0 text-center">
              Stripe payment integration coming soon
            </p>
          </div>
        </section>

        <Button type="submit" fullWidth size="lg">
          Place order
        </Button>
      </form>
    </div>
  );
}
